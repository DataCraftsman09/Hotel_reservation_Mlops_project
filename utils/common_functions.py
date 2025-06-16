import os 
import pandas 
from src.logger import get_logger
import yaml
import pandas as pd
from src.custom_exception import Custom_exception

logger = get_logger(__name__)

def read_yaml(file_path):
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found in the given path")
        
        with open(file_path,"r") as yaml_file:
            config = yaml.safe_load(yaml_file)
            logger.info("Successfully read the YAML File")
            return config
    except Exception as e:
        logger.error("ERROR : Reding the File")
        raise Custom_exception("Failed to read the Yaml File",e)

def Load_data(csv_path):
    try:
        logger.info("Loading Data")
        return pd.read_csv(csv_path)
    except Exception as e:
        logger.error(f"Error Loading the data {e}")
        raise Custom_exception("Failed to load the data", e)
    
