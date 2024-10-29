import traceback


def traceback_print_wrapper(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            print(traceback.format_exc())
            raise

    return wrapper
