from US_Visa.logger import logging
from US_Visa.exception import USvisaException
import sys

# logging.info("This is an info message.")

try:
    a = 1 / 0
except Exception as e:
    # Log the error message
    logging.error("An error occurred", exc_info=True)
    # Raise a custom exception with detailed error context
    raise USvisaException(e, sys) from e
