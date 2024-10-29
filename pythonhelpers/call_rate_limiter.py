import time


RATE_LIMIT_INTERVAL = 0.01


def rate_limit(interval: float = RATE_LIMIT_INTERVAL):
    def decorator(func):
        last_call_time = 0.0

        def wrapper(*args, **kwargs):
            nonlocal last_call_time
            now = time.time()
            if now - last_call_time >= RATE_LIMIT_INTERVAL:
                last_call_time = now
                return func(*args, **kwargs)

        return wrapper

    return decorator
