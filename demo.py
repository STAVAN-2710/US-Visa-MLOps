from US_Visa.logger import logging
from US_Visa.exception import USvisaException
import sys
from dotenv import load_dotenv  # Load environment variables from the .env file.
import os
from datetime import date

from US_Visa.pipeline.training_pipeline import TrainPipeline

obj = TrainPipeline()
obj.run_pipeline()
# try:
#     a = 1 / 0
# except Exception as e:
#     # Log the error message
#     logging.error("An error occurred", exc_info=True)
#     # Raise a custom exception with detailed error context
#     raise USvisaException(e, sys) from e
