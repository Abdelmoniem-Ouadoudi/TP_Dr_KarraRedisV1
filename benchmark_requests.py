import requests
import time

def benchmark(endpoint, num_requests):
    total_time = 0

    for i in range(num_requests):
        start_time = time.time()
        response = requests.get(endpoint)
        end_time = time.time()

        if response.status_code == 200:
            total_time += (end_time - start_time)
        else:
            print(f"Request {i + 1} failed with status code {response.status_code}")

    average_time = total_time / num_requests
    print(f"Average response time for {endpoint}: {average_time:.6f} seconds")

if __name__ == "__main__":
    num_requests = 100

    print("Benchmarking PostgreSQL endpoint...")
    benchmark("http://localhost:5000/query_postgres", num_requests)

    print("\nBenchmarking Redis endpoint...")
    benchmark("http://localhost:5000/query_redis", num_requests)