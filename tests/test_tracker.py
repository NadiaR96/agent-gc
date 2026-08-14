import json
import pytest
import typer.main
from datetime import datetime
from click.testing import CliRunner
from app.main import app

def test_cli_scan_command_triggers_garbage_collection_loop(tmp_path):
    # 1. Structure a temporary mock data asset on your local disk layout
    task_data = {
        "id": "TASK-12B",
        "purpose": "INFRASTRUCTURE_STATE_DRIFT_SCAN",
        "owner": "NADIA_SRE_ENGINEER",
        "created_at": datetime.utcnow().isoformat(),
        "ttl_days": 0,  # Force immediate expiration reaper path
        "run_count": 2,
        "status": "active"
    }
    
    mock_file = tmp_path / "task.json"
    mock_file.write_text(json.dumps(task_data))
    
    # 2. Extract Typer's underlying Click Command block cleanly
    click_command = typer.main.get_command(app)
    
    # 3. Invoke with catch_exceptions=False to let systems hooks evaluate natively
    runner = CliRunner()
    result = runner.invoke(
        click_command, 
        ["--file", str(mock_file)], 
        catch_exceptions=False
    )
    
    # 4. Assert your console output and exit code metrics match perfectly
    assert result.exit_code == 0
    assert "Task lifecycle status: REAPED" in result.output
    assert "Governance status: COMPLIANT" in result.output
