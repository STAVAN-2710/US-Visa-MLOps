import os
from US_Visa.constant import *
from dataclasses import dataclass
from datetime import datetime

# Generate a unique timestamp string used to version the artifacts for each pipeline run.
TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

# Define the configuration class for the overall training pipeline.
@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME  # Pipeline name, sourced from constants.
    # Combine the base artifact directory with the current timestamp to create a unique artifact directory.
    artifact_dir: str = os.path.join(ARTIFACT_DIR, TIMESTAMP)
    timestamp: str = TIMESTAMP          # Store the current timestamp for traceability.

# Create an instance of the training pipeline configuration so other components can use its settings.
training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

# Define the configuration class for the data ingestion component.
@dataclass
class DataIngestionConfig:
    # Set the directory for data ingestion artifacts by joining the pipeline's artifact_dir with the specific data ingestion folder.
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)
    # Define the file path for the feature store CSV by joining the data ingestion directory with subdirectory and file name.
    feature_store_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR, FILE_NAME)
    # Define the training set file path similarly within the ingested data subdirectory.
    training_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TRAIN_FILE_NAME)
    # Define the testing set file path similarly within the ingested data subdirectory.
    testing_file_path: str = os.path.join(data_ingestion_dir, DATA_INGESTION_INGESTED_DIR, TEST_FILE_NAME)
    # Specify the proportion of the data that will be split into testing data.
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    # Define the MongoDB collection name for data ingestion.
    collection_name: str = DATA_INGESTION_COLLECTION_NAME


@dataclass
class DataValidationConfig:
    data_validation_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_VALIDATION_DIR_NAME)
    drift_report_file_path: str = os.path.join(data_validation_dir, DATA_VALIDATION_DRIFT_REPORT_DIR, DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)