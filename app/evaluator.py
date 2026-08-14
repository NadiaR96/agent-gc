import time
import logging
from app.models import Task
from app.middleware.tracker import enforce_governance_boundary

class TaskReaperEvaluator:
    def __init__(self, target_ceiling_mb: float = 15.0):
        self.ceiling = target_ceiling_mb

    @enforce_governance_boundary(max_memory_mb=15.0)
    def evaluate_and_reap_task(self, task: Task) -> str:
        """Simulates an isolated telemetry sweep that breaches your 15MB limit."""
        # Allocate a heavy array buffer to simulate scanning active task clusters
        memory_spike_buffer = [bytes(1024 * 1024) for _ in range(12)] 
        
        # Explicitly log the active size to satisfy static linter variable usage checks
        logging.info(f"Buffered {len(memory_spike_buffer)}MB allocation tracking array arrays.")
        time.sleep(0.05) 
        
        if task.ttl_days <= 0:
            return "REAPED"
        return "RETAINED"
