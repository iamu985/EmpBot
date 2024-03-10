from src.utils.logger import Logger


def handle_log(logger: Logger):
    def inner_function(func, *args, **kwargs):
        def maintain_function_name(*args, **kwargs):
            logger.set_func_name(func.__name__)
            print(f"Setting function name {logger.get_func_name()} to the logger.")
            result = func(*args, **kwargs)
            logger.remove_func_name()
            print(f"Removing {func.__name__} from logger.")
            return result
        return maintain_function_name
    return inner_function