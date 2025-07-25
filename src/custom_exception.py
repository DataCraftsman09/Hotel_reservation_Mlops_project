import traceback
import sys

class Custom_exception(Exception):

    def __init__(self,error_message , error_detail):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message,error_detail)
    
    @staticmethod
    def get_detailed_error_message(error_message, error_detail):
        
        _ , _ , exc_tb = traceback.sys.exc_info()
        filename = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno


        return f"Error in {filename}, line {line_number} : {error_message}"
    

    def __str__(self) -> str:
        return self.error_message