from time import perf_counter


def precise_sleep(duration: float) -> None:
    """
    Sleep for a more precise duration using perf_counter.

    Parameters:
        duration (float): Time to sleep in seconds (can be fractional).
    """
    start_time = perf_counter()
    while perf_counter() - start_time < duration:
        pass
