#!/usr/bin/env python3
import os
import sys
import time
import requests

SERVER = os.environ.get("SUPERPLATFORM_SERVER", "http://127.0.0.1:8000")

def submit(command, project="default"):
    r = requests.post(
        SERVER + "/command",
        json={"command": command, "project": project, "auto_fix": True},
        timeout=20,
    )
    r.raise_for_status()
    return r.json()["job_id"]

def wait(job_id):
    while True:
        r = requests.get(SERVER + "/jobs/" + job_id, timeout=20)
        r.raise_for_status()
        job = r.json()
        print(f"[{job['status']}] {job_id}")
        if job["status"] not in ("queued", "running"):
            print("\nRESULT:")
            print(job.get("message", ""))
            print("stdout:", job.get("stdout", ""))
            print("stderr:", job.get("stderr", ""))
            return job
        time.sleep(2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Usage: python sp.py "your command"')
        sys.exit(1)
    job = submit(" ".join(sys.argv[1:]))
    wait(job)
