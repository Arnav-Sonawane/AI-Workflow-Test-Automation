import requests
import time

BASE_URL = "https://jsonplaceholder.typicode.com"

# How fast each API should respond (in seconds)
MAX_RESPONSE_TIME = 3.0

# Test 1: Check how fast the posts API responds
def test_posts_response_time():
    start = time.time()
    response = requests.get(f"{BASE_URL}/posts")
    end = time.time()
    
    response_time = end - start
    print(f"\n Posts API responded in: {response_time:.2f} seconds")
    
    assert response_time < MAX_RESPONSE_TIME, f"Too slow! Took {response_time:.2f}s, limit is {MAX_RESPONSE_TIME}s"

# Test 2: Check how fast a single post API responds
def test_single_post_response_time():
    start = time.time()
    response = requests.get(f"{BASE_URL}/posts/1")
    end = time.time()
    
    response_time = end - start
    print(f"\n Single post API responded in: {response_time:.2f} seconds")
    
    assert response_time < MAX_RESPONSE_TIME, f"Too slow! Took {response_time:.2f}s, limit is {MAX_RESPONSE_TIME}s"

# Test 3: Check performance across 5 back to back requests
def test_multiple_requests_performance():
    times = []
    
    for i in range(5):
        start = time.time()
        requests.get(f"{BASE_URL}/posts/{i+1}")
        end = time.time()
        times.append(end - start)
    
    average_time = sum(times) / len(times)
    print(f"\n Average response time over 5 requests: {average_time:.2f} seconds")
    
    assert average_time < MAX_RESPONSE_TIME, f"Average too slow: {average_time:.2f}s"