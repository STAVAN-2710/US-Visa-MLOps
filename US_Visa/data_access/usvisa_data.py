# Import the MongoDBClient class that handles database connections
from US_Visa.configuration.mongo_db_connection import MongoDBClient  
# Import the constant for the database name from the constants file
from US_Visa.constant import DATABASE_NAME  
# Import a custom exception class to wrap and raise exceptions in a consistent manner
from US_Visa.exception import USvisaException  
# Import pandas for handling data frames
import pandas as pd  
# Import sys to pass system-specific parameters (e.g., traceback info) in exception handling
import sys  
# Import Optional type hint for an optional parameter
from typing import Optional  
# Import numpy for numeric operations such as replacing specific values
import numpy as np  



class USvisaData:
    """
    This class helps export the entire MongoDB collection as a pandas DataFrame.
    It encapsulates the logic for connecting to MongoDB, retrieving data, and 
    converting the result into a clean DataFrame by removing unwanted columns and 
    replacing placeholder values.
    """

    def __init__(self):
        """
        Initialize the USvisaData instance by attempting to create a MongoDB client.
        If the connection fails, a custom USvisaException is raised.
        """
        try:
            # Create an instance of MongoDBClient using a pre-defined database name constant.
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            # Raise a custom exception with system details for improved error handling.
            raise USvisaException(e, sys)
        

    def export_collection_as_dataframe(self, collection_name: str, database_name: Optional[str] = None) -> pd.DataFrame:
        """
        Export an entire MongoDB collection as a pandas DataFrame.
        
        Parameters:
            collection_name (str): Name of the MongoDB collection to export.
            database_name (Optional[str]): Optional; if provided, use this database,
                                           otherwise use the default from mongo_client.
        
        Returns:
            pd.DataFrame: DataFrame containing all documents from the specified collection,
                          with the "_id" column dropped and "na" strings replaced with np.nan.
        """
        try:
            # Determine which database to use: if a database_name is provided, use it; 
            # otherwise, use the default database from the MongoDB client.
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client[database_name][collection_name]

            # Retrieve all documents in the collection, convert the cursor to a list, and then into a DataFrame.
            df = pd.DataFrame(list(collection.find()))
            
            # If the DataFrame contains the MongoDB default "_id" field, drop it as it's not needed.
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)
            
            # Replace any occurrence of the string "na" with numpy's NaN for consistent missing data representation.
            df.replace({"na": np.nan}, inplace=True)
            
            # Return the cleaned DataFrame.
            return df
        except Exception as e:
            # Wrap and raise any exception encountered using the custom USvisaException.
            raise USvisaException(e, sys)
