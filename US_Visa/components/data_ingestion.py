import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from US_Visa.entity.config_entity import DataIngestionConfig
from US_Visa.entity.artifact_entity import DataIngestionArtifact
from US_Visa.exception import USvisaException
from US_Visa.logger import logging
from US_Visa.data_access.usvisa_data import USvisaData

class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        """
        Initialize the DataIngestion instance with a configuration.
        :param data_ingestion_config: Configuration object containing paths, collection name, split ratio, etc.
        """
        try:
            # Save the provided data ingestion configuration for later use
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            # Wrap any exception in a custom USvisaException for consistency across the project
            logging.error(f"Error occurred while initializing DataIngestion: {e}")
            raise USvisaException(e, sys)

    def export_data_into_feature_store(self) -> DataFrame:
        """
        Method Name : export_data_into_feature_store
        Description : Exports data from MongoDB by reading the specified collection and then converts it into a CSV file.
        Output      : Returns the data as a pandas DataFrame and stores the CSV in the configured feature store path.
        On Failure  : Logs the exception and raises a USvisaException.
        """
        try:
            # Log the start of the data export process from MongoDB
            logging.info("Exporting data from mongodb")
            # Create an instance of USvisaData to handle MongoDB connection and data retrieval
            usvisa_data = USvisaData()
            # Export the entire collection as a DataFrame using the collection name from the configuration
            dataframe = usvisa_data.export_collection_as_dataframe(
                collection_name=self.data_ingestion_config.collection_name
            )
            # Log the shape of the retrieved DataFrame for verification purposes
            logging.info(f"Shape of dataframe: {dataframe.shape}")
            # Retrieve the file path where the feature store CSV should be saved from the configuration
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # Extract the directory path from the file path
            dir_path = os.path.dirname(feature_store_file_path)
            # Create the directory if it does not already exist (ensuring compatibility across platforms)
            os.makedirs(dir_path, exist_ok=True)
            # Log the file path where data will be saved
            logging.info(f"Saving exported data into feature store file path: {feature_store_file_path}")
            # Save the DataFrame to a CSV file without the index and with headers
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            # Return the DataFrame for downstream processing
            return dataframe
        except Exception as e:
            # If any exception occurs, wrap it in a custom exception and raise it
            logging.error(f"Error occurred while exporting data into feature store: {e}")
            raise USvisaException(e, sys)

    def split_data_as_train_test(self, dataframe: DataFrame) -> None:
        """
        Method Name : split_data_as_train_test
        Description : Splits the given DataFrame into training and testing sets based on the configured split ratio.
        Output      : Saves the train and test sets as CSV files in the specified paths.
        On Failure  : Logs the error and raises a USvisaException.
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class")
        try:
            # Use train_test_split (typically from sklearn.model_selection) to split the data
            train_set, test_set = train_test_split(
                dataframe, test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("Performed train test split on the dataframe")
            logging.info("Exited split_data_as_train_test method of Data_Ingestion class")
            # Obtain the directory path for the training file from the configuration
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            # Create the directory if it doesn't exist, ensuring that file save operation will succeed
            os.makedirs(dir_path, exist_ok=True)
            logging.info("Exporting train and test file path.")
            # Save the train and test datasets to CSV files with headers and without an index column
            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            logging.info("Exported train and test file path.")
        except Exception as e:
            # Use exception chaining to provide complete traceback information with custom exception
            raise USvisaException(e, sys) from e

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Method Name : initiate_data_ingestion
        Description : Orchestrates the data ingestion process. It exports data from MongoDB,
                      splits it into training and testing sets, and returns these paths as an artifact.
        Output      : Returns a DataIngestionArtifact containing paths to the training and test CSV files.
        On Failure  : Logs any error encountered and raises a USvisaException.
        """
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        try:
            # First, export the data from MongoDB into the feature store and obtain it as a DataFrame
            dataframe = self.export_data_into_feature_store()
            logging.info("Got the data from mongodb")
            # Next, split the DataFrame into training and testing sets and save them to CSV files
            self.split_data_as_train_test(dataframe)
            logging.info("Performed train test split on the dataset")
            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")
            # Create an artifact object encapsulating the paths of the training and testing data
            data_ingestion_artifact = DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            # Log the details of the artifact for tracking purposes
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            # Return the artifact so that downstream components can make use of this data
            return data_ingestion_artifact
        except Exception as e:
            # If an error occurs, wrap it in the custom exception and raise it
            raise USvisaException(e, sys) from e