import os 
import sys

import numpy as np 
import dill # Dill is used for serialization (not directly used in these functions)
import yaml 
from pandas import DataFrame 

from US_Visa.exception import USvisaException
from US_Visa.logger import logging

def read_yaml_file(file_path: str) -> dict:
    """
        Parameters:
    - file_path (str): The full path to the YAML file.

    Returns:
    - dict: The parsed contents of the YAML file.

    Raises:
    - USvisaException: If there is any error while reading or parsing the file.
    """
    try:
        # Open the YAML file in binary mode ('rb')
        with open(file_path, "rb") as yaml_file:
            # Use safe_load to parse the YAML file into a Python dictionary in a secure manner
            return yaml.safe_load(yaml_file)
    except Exception as e:
        # If any exception occurs, raise a custom USvisaException with traceback info using sys
        logging.error("Error reading YAML file", exc_info=True)
        raise USvisaException(e, sys) from e

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """ 
    Parameters:
    - file_path (str): The destination path for the YAML file.
    - content (object): The content to be serialized and written to the file (should be YAML-serializable).
    - replace (bool): If True, replace the existing file at file_path. Default is False.

    Raises:
    - USvisaException: If there is any error while writing the file.
    """
    try:
        if replace:
            # If the replace flag is True and the file already exists, remove it first.
            if os.path.exists(file_path):
                os.remove(file_path)
        # Ensure that the directory for the file exists; create it if needed.
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Open the file in write mode ('w') to dump the YAML content.
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        # Raise a custom exception to signal a failure with detailed traceback information.
        logging.error("Error writing YAML file", exc_info=True)
        raise USvisaException(e, sys) from e
    

def load_object(file_path: str) -> object:
    # Log entry into the load_object function for traceability
    logging.info("Entered the load_object method of utils")
    try:
        # Open the file in binary read mode so that the serialized object can be read
        with open(file_path, "rb") as file_obj:
            # Deserialize the object stored in the file using dill
            obj = dill.load(file_obj)
        # Log successful exit from the method
        logging.info("Exited the load_object method of utils")
        # Return the deserialized object
        return obj
    except Exception as e:
        # If any error occurs, wrap it in a custom USvisaException with traceback details
        logging.error("Error loading object", exc_info=True)
        raise USvisaException(e, sys) from e
    
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Parameters:
    - file_path: str -> The file path where the numpy array will be saved.
    - array: np.array -> The numpy array data to save.
    """
    try:
        # Extract the directory path from the file path
        dir_path = os.path.dirname(file_path)
        # Create the directory if it does not exist already (ensuring cross-platform compatibility)
        os.makedirs(dir_path, exist_ok=True)
        # Open the target file in binary write mode
        with open(file_path, 'wb') as file_obj:
            # Save the numpy array to the file using np.save, which writes it in binary format
            np.save(file_obj, array)
    except Exception as e:
        # If an error occurs, wrap it in a custom exception for consistent error handling
        logging.error("Error saving numpy array data", exc_info=True)
        raise USvisaException(e, sys) from e
    
def load_numpy_array_data(file_path: str) -> np.array:
    """
        Parameters:
    - file_path: str -> The file path from which to load the numpy array.

    Returns:
    - np.array -> The loaded numpy array data.
    """
    try:
        # Open the file containing the numpy array in binary read mode
        with open(file_path, 'rb') as file_obj:
            # Load and return the numpy array from the file using np.load
            return np.load(file_obj)
    except Exception as e:
        # Wrap and re-raise any exceptions using the custom USvisaException for unified error logging
        logging.error("Error loading numpy array data", exc_info=True)
        raise USvisaException(e, sys) from e