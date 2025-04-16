import os
from datetime import date
from dotenv import load_dotenv  # Load environment variables from the .env file.

# Load environment variables from the .env file
load_dotenv()

# General Database and Collection Configuration
DATABASE_NAME = "US_VISA"            # Name of the MongoDB database. Centralizes the config for easy updates.
COLLECTION_NAME = "visa_data"        # Name of the collection within the database holding visa-related data.

# Retrieve the MongoDB connection URL from the environment variable.
# Note: Typically, you would pass a string key like "MONGODB_URL_KEY". Here, ensure that MONGODB_URL_KEY is defined appropriately in your environment.
MONGODB_URL_KEY = os.getenv("MONGODB_URL_KEY")

# Pipeline and Artifact Naming Constants
PIPELINE_NAME: str = "usvisa"        # Name of the ML pipeline. Useful in logging and tracking different pipeline runs.
ARTIFACT_DIR: str = "artifact"       # Base directory to store artifacts generated during pipeline runs (e.g., logs, models, data splits).

# File Names for Data and Model Artifacts
TRAIN_FILE_NAME: str = "train.csv"   # File name for the training dataset generated during data ingestion.
TEST_FILE_NAME: str = "test.csv"     # File name for the testing dataset generated during data ingestion.
FILE_NAME: str = "usvisa.csv"        # Raw data file name that may be ingested from MongoDB before processing.
MODEL_FILE_NAME = "model.pkl"        # File name for the serialized model artifact post training.

"""
Data Ingestion related constants
This section defines variables used specifically during the data ingestion process.
"""
DATA_INGESTION_COLLECTION_NAME: str = "visa_data"  # Name of the collection from which data is ingested; note it could be reused or different.
DATA_INGESTION_DIR_NAME: str = "data_ingestion"      # Base folder for all data ingestion artifacts, ensuring organized outputs.
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"  # Subdirectory to store processed feature data for downstream tasks.
DATA_INGESTION_INGESTED_DIR: str = "ingested"        # Subdirectory to store the final output of the ingested data (e.g., after train/test split).
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: float = 0.2   # Ratio defining the fraction of data reserved for testing; facilitates consistent train/test splits.

