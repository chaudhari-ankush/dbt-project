from fastapi import FastAPI
import subprocess
import os

app = FastAPI()

@app.get("/run-dbt-model")
def run_dbt_model():
    dbt_dir = os.path.join(os.path.dirname(__file__), "..", "dbt")
    try:
        result = subprocess.run([
            "dbt", "run", "--project-dir", dbt_dir
        ], capture_output=True, text=True, check=True)
        return {"status": "success", "output": result.stdout}
    except subprocess.CalledProcessError as e:
        return {"status": "error", "output": e.stderr} 