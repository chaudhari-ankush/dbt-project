from fastapi import FastAPI
import subprocess

app = FastAPI()

def run_dbt_command(args):
    try:
        result = subprocess.run(
            ["dbt"] + args,
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

@app.get("/dbt/run")
def dbt_run():
    return run_dbt_command(["run"])

@app.get("/dbt/debug")
def dbt_debug():
    return run_dbt_command(["debug"])

@app.get("/dbt/docs")
def dbt_docs():
    return run_dbt_command(["docs", "generate"]) 