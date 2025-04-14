import os  # For file and directory operations
import sys  # For system-specific functions and exception handling

def error_message_detail(error, error_detail: sys):
    """
    Generates a detailed error message with file name, line number, and error description.

    Parameters:
    - error: The original exception object.
    - error_detail: System-specific traceback information from sys.exc_info().

    Returns:
    - A formatted string containing error details.
    """
    # Extract traceback information (file name, line number)
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename

    # Format the error message with context
    error_message = "Error occurred in script [{0}] at line [{1}] with message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message

class USvisaException(Exception):
    """
    Custom exception class for handling errors in the US Visa project.

    Enhances standard Python exceptions by providing detailed context about
    where the error occurred (file name and line number).
    """
    
    def __init__(self, error_message, error_detail):
        """
        Initializes the custom exception with an enhanced error message.

        Parameters:
        - error_message: A brief description of the error.
        - error_detail: System-specific traceback information from sys.exc_info().
        """
        super().__init__(error_message)
        
        # Generate a detailed error message using the helper function
        self.error_message = error_message_detail(
            error_message, 
            error_detail=error_detail
        )

    def __str__(self):
        """
        Returns the detailed error message when the exception is printed.
        """
        return self.error_message
