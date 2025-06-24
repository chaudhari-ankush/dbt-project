from fastapi import FastAPI, HTTPException, BackgroundTasks, Query
from dbt.cli.main import dbtRunner, dbtRunnerResult
import os
import logging
import json
from typing import Dict, Any, List, Optional
from pydantic import BaseModel
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

app = FastAPI(
    title="DBT Core API Service",
    description="API service for executing dbt-core commands",
    version="1.0.0"
)

class DBTCommand(BaseModel):
    command: str
    args: Optional[List[str]] = None
    vars: Optional[Dict[str, Any]] = None
    profiles_dir: Optional[str] = None
    project_dir: Optional[str] = None
    target: Optional[str] = None

class DBTResponse(BaseModel):
    success: bool
    message: str
    results: Optional[Any] = None
    error: Optional[str] = None

@app.get("/")
async def root() -> Dict[str, str]:
    return {"message": "DBT Core API Service is running"}

@app.get("/health")
async def health_check() -> Dict[str, str]:
    return {"status": "healthy"}

@app.post("/dbt/run", response_model=DBTResponse)
async def run_dbt_command(command: DBTCommand, background_tasks: BackgroundTasks) -> DBTResponse:
    try:
        logger.info(f"Received dbt command: {command.command}")
        
        # Initialize dbt runner
        dbt = dbtRunner()
        
        # Prepare command arguments
        args = [command.command]
        if command.args:
            args.extend(command.args)
            
        # Add optional parameters
        if command.profiles_dir:
            args.extend(["--profiles-dir", command.profiles_dir])
        if command.project_dir:
            args.extend(["--project-dir", command.project_dir])
        if command.target:
            args.extend(["--target", command.target])
        if command.vars:
            args.extend(["--vars", json.dumps(command.vars)])
            
        logger.info(f"Executing dbt command with args: {args}")
        
        # Run dbt command
        res: dbtRunnerResult = dbt.invoke(args)
        
        if res.success:
            logger.info("DBT command executed successfully")
            return DBTResponse(
                success=True,
                message="DBT command executed successfully",
                results=res.results
            )
        else:
            logger.error(f"DBT command failed: {res.results}")
            return DBTResponse(
                success=False,
                message="DBT command failed",
                results=res.results,
                error=str(res.results)
            )
            
    except Exception as e:
        logger.error(f"Error executing DBT command: {str(e)}")
        return DBTResponse(
            success=False,
            message="Error executing DBT command",
            error=str(e)
        )

@app.get("/dbt/available-commands")
async def get_available_commands() -> Dict[str, List[str]]:
    """Return list of available dbt commands"""
    return {
        "commands": [
            "run",
            "test",
            "seed",
            "snapshot",
            "compile",
            "docs generate",
            "docs serve",
            "debug",
            "deps",
            "clean",
            "ls",
            "show"
        ]
    }

@app.get("/dbt/run-model", response_model=DBTResponse)
async def run_dbt_model(
    model: str = Query(..., description="Name of the dbt model to run"),
    project_dir: Optional[str] = Query(None, description="Path to dbt project"),
    profiles_dir: Optional[str] = Query(None, description="Path to profiles directory"),
    target: Optional[str] = Query(None, description="dbt target profile")
) -> DBTResponse:
    """
    Run a specific dbt model using a GET request.
    """
    try:
        logger.info(f"Received request to run model: {model}")
        dbt = dbtRunner()
        args = ["run", "--select", model]
        if profiles_dir:
            args.extend(["--profiles-dir", profiles_dir])
        if project_dir:
            args.extend(["--project-dir", project_dir])
        if target:
            args.extend(["--target", target])
        logger.info(f"Executing dbt run with args: {args}")
        res: dbtRunnerResult = dbt.invoke(args)
        if res.success:
            logger.info("DBT model run successfully")
            return DBTResponse(
                success=True,
                message=f"DBT model '{model}' run successfully",
                results=res.results
            )
        else:
            logger.error(f"DBT model run failed: {res.results}")
            return DBTResponse(
                success=False,
                message=f"DBT model '{model}' run failed",
                results=res.results,
                error=str(res.results)
            )
    except Exception as e:
        logger.error(f"Error running DBT model: {str(e)}")
        return DBTResponse(
            success=False,
            message="Error running DBT model",
            error=str(e)
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    ) 