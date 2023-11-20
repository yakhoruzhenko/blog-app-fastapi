import cProfile
import functools
import os
import pstats
from typing import Any, Callable

from typing_extensions import ParamSpec

P = ParamSpec('P')  # To represent the arguments of the wrapped function


def profile_func(func: Callable[P, Any]) -> Callable[P, Any]:
    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        output_folder = 'profiling_results'
        os.makedirs(output_folder, exist_ok=True)
        output_file = os.path.join(output_folder, 'report.txt')
        with open(output_file, 'a') as file:
            stats = pstats.Stats(profiler, stream=file)
            stats.sort_stats('cumtime')
            print(f'{func.__name__}', file=file)
            stats.print_stats(10)  # top ten results sorted by cumtime
        return result
    return wrapper
