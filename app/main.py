from fastapi import FastAPI, Query
import subprocess
import os

app = FastAPI()

def dbt_run_selected(models):
    dbt_dir = os.path.join(os.path.dirname(__file__), "..", "dbt")
    args = ["dbt", "run", "--project-dir", dbt_dir]
    if models:
        args += ["--select"] + models
    try:
        result = subprocess.run(
            args,
            capture_output=True, text=True, check=True
        )
        return {"status": "success", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "output": e.stderr}

@app.get("/run")
def run_models(models: str = Query(None, description="Comma-separated list of model names to run (e.g. model1,model2)")):
    model_list = [m.strip() for m in models.split(",")] if models else []
    return dbt_run_selected(model_list) 