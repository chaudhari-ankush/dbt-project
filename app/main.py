from fastapi import FastAPI
import subprocess

app = FastAPI()

def run_dbt_iceberg():
    try:
        result = subprocess.run(
            ["dbt", "run", "--select", "sample_iceberg_model"],
            capture_output=True,
            text=True,
            check=True
        )
        return {"success": True, "stdout": result.stdout, "stderr": result.stderr}
    except subprocess.CalledProcessError as e:
        return {"success": False, "stdout": e.stdout, "stderr": e.stderr}

@app.get("/")
def health():
    return {"status": "ok"}

@app.get("/dbt/run-iceberg")
def dbt_run_iceberg():
    return run_dbt_iceberg() 