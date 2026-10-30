import importlib.util
from pathlib import Path

LOCUSTFILE = Path(__file__).resolve().parents[1] / "locust" / "locustfile.py"
SPEC = importlib.util.spec_from_file_location("project_locustfile", LOCUSTFILE)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_load_user_defines_three_weighted_scenarios():
    tasks = [
        value for value in MODULE.StorefrontLoadUser.__dict__.values()
        if callable(value) and hasattr(value, "locust_task_weight")
    ]
    assert len(tasks) == 3
    assert sorted(task.locust_task_weight for task in tasks) == [1, 3, 5]
