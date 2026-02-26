from fastapi import FastAPI, UploadFile, File, HTTPException
import os

# optional persistence layer
from sqlalchemy import create_engine, Column, String, JSON, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from crewai import Crew
from agents import agents as AGENTS
from task import TASKS

# optionally configure Celery if Redis is available
try:
    from celery import Celery

    celery_app = Celery('financial', broker='redis://localhost:6379/0')

    @celery_app.task
    def async_analyze(pdf_path: str, pdf_name: str):
        crew = Crew(agents=AGENTS, tasks=TASKS)
        result = crew.kickoff(inputs={"pdf_path": pdf_path})
        # store to database as well
        try:
            db = SessionLocal()
            db.add(Analysis(pdf_name=pdf_name, result=result))
            db.commit()
        except Exception:
            pass
        return result
except ImportError:
    celery_app = None

# set up simple SQLite database to save analysis results
Base = declarative_base()


class Analysis(Base):
    __tablename__ = 'analyses'
    id = Column(Integer, primary_key=True)
    pdf_name = Column(String)
    result = Column(JSON)


engine = create_engine('sqlite:///results.db', connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

app = FastAPI(title="Financial Document Analyzer")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_pdf(file: UploadFile = File(...)):
    """Endpoint that accepts a multipart PDF file and returns crew analysis."""

    # save incoming file to disk
    os.makedirs("data", exist_ok=True)
    path = f"data/{file.filename}"
    try:
        with open(path, "wb") as f:
            f.write(await file.read())

        # build crew and run either synchronously or asynchronously
        if celery_app:
            # dispatch background celery job
            async_analyze.delay(path, file.filename)
            return {"status": "queued", "file": file.filename}
        else:
            crew = Crew(agents=AGENTS, tasks=TASKS)
            result = crew.kickoff(inputs={"pdf_path": path})

            # persist the result
            try:
                db = SessionLocal()
                db.add(Analysis(pdf_name=file.filename, result=result))
                db.commit()
            except Exception:
                pass

            return {"analysis": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)