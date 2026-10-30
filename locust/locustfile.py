from locust import HttpUser, between, task


class StorefrontLoadUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task(5)
    def health_check(self):
        with self.client.get("/health", name="/health", catch_response=True) as response:
            if response.status_code != 200 or response.json().get("status") != "ok":
                response.failure("Health endpoint returned an unexpected response")

    @task(3)
    def browse_products(self):
        with self.client.get("/products", params={"limit": 20}, name="/products", catch_response=True) as response:
            if response.status_code != 200 or len(response.json()) != 20:
                response.failure("Product endpoint returned an unexpected result")

    @task(1)
    def compute_workload(self):
        with self.client.post(
            "/compute",
            json={"iterations": 1000},
            name="/compute",
            catch_response=True,
        ) as response:
            payload = response.json() if response.status_code == 200 else {}
            if payload.get("iterations") != 1000 or "checksum" not in payload:
                response.failure("Compute endpoint returned an unexpected result")
