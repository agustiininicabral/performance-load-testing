from locust import task

from locust.locustfile import StorefrontLoadUser


def test_load_user_defines_three_weighted_scenarios():
    tasks = [
        value for value in StorefrontLoadUser.__dict__.values()
        if callable(value) and hasattr(value, "locust_task_weight")
    ]
    assert len(tasks) == 3
    assert sorted(task.locust_task_weight for task in tasks) == [1, 3, 5]
