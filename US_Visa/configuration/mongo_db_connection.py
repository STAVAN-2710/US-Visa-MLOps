import sys                                      # Import the sys module for exception handling and traceback info.
from US_Visa.exception import USvisaException   # Import a custom exception to handle errors gracefully.
from US_Visa.logger import logging              # Import a custom logging utility to log informational and error messages.
import os                                       # OS module to interact with environment variables.
from US_Visa.constant import DATABASE_NAME, MONGODB_URL_KEY  # Import constants for the database name and MongoDB URL environment key.
import pymongo                                  # Import pymongo to connect to a MongoDB instance.
import certifi                                  # Import certifi to provide a set of root certificates for TLS connections.

# Obtain the path to the CA certificates from certifi.
ca = certifi.where()

class MongoDBClient:
    """
    Class Name    : MongoDBClient
    Description   : This class establishes a connection to the MongoDB database.
                    It checks if a connection already exists and reuses it, ensuring efficient resource usage.
                    The connection string is securely loaded from an environment variable.
    Output        : A connection to the specified MongoDB database.
    On Failure    : Raises a USvisaException if an error occurs during connection setup.
    """
    # Static attribute to hold the MongoClient instance so that it can be shared/reused across the application.
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            # If a MongoClient has not been instantiated, create a new connection.
            if MongoDBClient.client is None:
                # Retrieve the MongoDB connection URL from the environment variable.
                mongo_db_url = os.getenv("MONGODB_URL_KEY")
                # If the connection string is missing, raise an exception indicating the misconfiguration.
                if mongo_db_url is None:
                    raise Exception(f"Environment key: {MONGODB_URL_KEY} is not set.")
                # Create a new MongoClient using the connection URL and CA certificates for TLS verification.
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url, tlsCAFile=ca)
            # Assign the shared client instance to this object.
            self.client = MongoDBClient.client
            # Access the specified database in MongoDB.
            self.database = self.client[database_name]
            # Save the database name for possible future reference.
            self.database_name = database_name
            # Log the successful connection for informational purposes.
            logging.info("MongoDB connection succesfull")
        except Exception as e:
            # Any exception is caught and rethrown as a custom USvisaException, including system context.
            logging.error("Error connecting to MongoDB", exc_info=True)
            raise USvisaException(e, sys)
