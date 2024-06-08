import logging
import time


class LoggerDecoratorFactory:
    """
    Factory class to create logger time decorators
    """

    type = None

    def __init__(self, type):
        LoggerDecoratorFactory.type = type

    @classmethod
    def log_time(cls, func, name=None):
        """
        Decorator to log the time taken by the function
        :param name: the name of the table
        :param func: the function to decorate
        :return: the decorated function
        """
        logging.basicConfig(level=logging.INFO)

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logging.info(f"{cls.type}: Time taken by {func.__qualname__}: {end_time - start_time} seconds" + (f" - {name}" if name else ""))
            return result

        return wrapper
