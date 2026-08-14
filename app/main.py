import json
import typer
from pathlib import Path
from app.models import Task
from app.evaluator import TaskReaperEvaluator

# Initialize your high-velocity Typer CLI app context
app = typer.Typer(help="Agent-GC: Hardware-Constrained Task Lifecycle Compliance Tool.")

@app.command()
def scan(
    file: Path = typer.Option(..., exists=True, help="Path to the JSON task configuration ledger")
):
    """
    Scans a local JSON configuration ledger and evicts expired tasks under a 15MB ceiling.
    """
    reaper = TaskReaperEvaluator(target_ceiling_mb=15.0)
    
    try:
        # Load and parse your flat JSON file data rows natively
        with open(file, 'r') as f:
            raw_data = json.load(f)
            
        # Validate the raw map directly against your strict Pydantic model contract
        task = Task(**raw_data)
        typer.echo(f"[SYSTEM] Auditing active task structure: {task.id} (Owner: {task.owner})")
        
        # Execute the heavy validation sweep wrapped inside your memory-isolation decorator
        outcome = reaper.evaluate_and_reap_task(task)
        typer.echo(f"[OUTCOME] Task lifecycle status: {outcome} | Governance status: COMPLIANT")
        
    except Exception as exc:
        typer.echo(f"[ERROR] Governance boundary processing crash: {str(exc)}", err=True)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
