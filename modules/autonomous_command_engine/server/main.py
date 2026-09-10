from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from pathlib import Path
from uuid import uuid4
from datetime import datetime, timezone
import subprocess
import threading
import json

app = FastAPI(title="SuperPlatform Autonomous Command Engine", version="0.1.0")

BASE = Path(__file__).resolve().parent
WORK = BASE / "workspace"
JOBS = BASE / "jobs"
WORK.mkdir(exist_ok=True)
JOBS.mkdir(exist_ok=True)

ALLOWED_ACTIONS = {
    "python_test": ["python", "-m", "compileall", "-q"],
}

class CommandRequest(BaseModel):
    command: str = Field(min_length=1, max_length=4000)
    project: str = "default"
    auto_fix: bool = True

def now():
    return datetime.now(timezone.utc).isoformat()

def save_job(job):
    (JOBS / f"{job['id']}.json").write_text(
        json.dumps(job, indent=2), encoding="utf-8"
    )

def run_job(job_id):
    job = json.loads((JOBS / f"{job_id}.json").read_text())
    job["status"] = "running"
    job["started_at"] = now()
    save_job(job)

    try:
        # Controlled task routing. Expand this registry with explicit worker actions.
        command = job["command"].lower()

        if "test" in command or "check" in command:
            target = WORK / job["project"]
            target.mkdir(parents=True, exist_ok=True)
            proc = subprocess.run(
                ALLOWED_ACTIONS["python_test"] + [str(target)],
                capture_output=True,
                text=True,
                timeout=120,
            )
            job["exit_code"] = proc.returncode
            job["stdout"] = proc.stdout[-12000:]
            job["stderr"] = proc.stderr[-12000:]
            job["status"] = "passed" if proc.returncode == 0 else "failed"
        else:
            job["status"] = "needs_worker"
            job["message"] = (
                "No controlled worker action matches this command yet. "
                "Add a dedicated action adapter instead of enabling arbitrary shell execution."
            )

    except subprocess.TimeoutExpired:
        job["status"] = "timeout"
        job["message"] = "Worker exceeded the time limit."
    except Exception as e:
        job["status"] = "error"
        job["message"] = str(e)

    job["finished_at"] = now()
    save_job(job)

@app.get("/health")
def health():
    return {"status": "ok", "service": "autonomous-command-engine"}

@app.post("/command")
def submit(req: CommandRequest):
    job_id = str(uuid4())
    job = {
        "id": job_id,
        "command": req.command,
        "project": req.project,
        "auto_fix": req.auto_fix,
        "status": "queued",
        "created_at": now(),
    }
    save_job(job)
    threading.Thread(target=run_job, args=(job_id,), daemon=True).start()
    return {"job_id": job_id, "status": "queued"}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    path = JOBS / f"{job_id}.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Job not found")
    return json.loads(path.read_text())
