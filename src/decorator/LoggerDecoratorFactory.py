import logging
import time


class LoggerDecoratorFactory:
    """
    Factory class to create logger time decorators
    """

    @classmethod
    def log_time(cls, func):
        """
        Decorator to log the time taken by the function
        :param func: the function to decorate
        :return: the decorated function
        """
        logging.basicConfig(level=logging.INFO)

        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logging.info(f"Time taken by {func.__qualname__}: {end_time - start_time} seconds")
            return result

        return wrapper
