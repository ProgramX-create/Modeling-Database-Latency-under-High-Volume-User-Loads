# app_crash_test.py
# A script to test how fast a server slows down when traffic spikes

import time
import random

class ServerTester:
    def __init__(self):
        self.normal_speed_ms = 15.0 
        print("[START] Loading server stress test...")

    def simulate_users(self, total_users):
        print(f"\n[TESTING] Sending {total_users} users to the app at the same time...")
        
        # Figure out the lag multiplier based on how crowded it gets
        if total_users <= 100:
            lag_multiplier = 1.0
        elif total_users <= 1000:
            lag_multiplier = 2.5
        else:
            # Fake a massive bottleneck spike
            lag_multiplier = (total_users / 200) ** 2

        total_lag = 0
        crashed_apps = 0
        
        for i in range(total_users):
            # Calculate final response speed with some random bounce
            user_speed = (self.normal_speed_ms * lag_multiplier) + random.uniform(1, 5)
            # Anything over 150ms feels frozen or broken to a user
            if user_speed > 150.0:
                crashed_apps += 1
            total_lag += user_speed
        avg_speed = round(total_lag / total_users, 2)
        crash_rate = round((crashed_apps / total_users) * 100, 2)

        if crash_rate > 20.0:
            system_status = "SERVER CRASHED / TOO SLOW"
        else:
            system_status = "RUNNING PERFECTLY"

        return {
            "users": total_users,
            "avg_speed_ms": avg_speed,
            "crash_percent": crash_rate,
            "status": system_status
        }
if __name__ == "__main__":
    tester = ServerTester()
     # Test 1: Try a normal crowd (100 people)
    result1 = tester.simulate_users(100)
    print(f"Status: {result1['status']}")
    print(f"Average Speed: {result1['avg_speed_ms']} ms")
    print(f"Apps Frozen: {result1['crash_percent']}%")
    # Test 2: Try a viral spike (2500 people all at once)
    result2 = tester.simulate_users(2500)
    print(f"Status: {result2['status']}")
    print(f"Average Speed: {result2['avg_speed_ms']} ms")
    print(f"Apps Frozen: {result2['crash_percent']}%")
