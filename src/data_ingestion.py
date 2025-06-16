import os 
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import Custom_exception
from config.paths_config import *
from utils.common_functions import read_yaml

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self, config):
        self.config = config["data_ingestion"]
        self.bucket_name = self.config["bucket_name"]
        self.file_name = self.config["bucket_file_name"]
        self.train_ratio = self.config["train_ratio"]

        os.makedirs(RAW_DIR,exist_ok=True)

        logger.info(f"Data Ingestion Started with {self.bucket_name} and file is {self.file_name}")

    def download_csv_from_gcp(self):
        try:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "F:\\MLOPS\\GCP_KEYS\\focus-vim-461708-m6-7819a71c7091.json"
            client = storage.Client()
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)
            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"Succesfully DownLoaded Filename : {self.file_name} to fileath : {RAW_FILE_PATH}")

        except Exception as e:
            logger.info("Error while downloading the csv file")
            raise Custom_exception("Failed to download csv file ",e)
    def split_data(self):
        try:
            logger.info("Starting Spliting the data")
            data = pd.read_csv(RAW_FILE_PATH)

            train_data , test_data = train_test_split(data, test_size=1 - self.train_ratio,random_state=42)

            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)

            logger.info(f"train data saved to {TRAIN_FILE_PATH}")
            logger.info(f"test data saved to {TEST_FILE_PATH}")

        except Exception as e:
            logger.info("Error while Splitting data")
            raise Custom_exception("Failed to split data into train and test set ",e)

    def run(self):
        try:
            logger.info("started data ingestion process")

            self.download_csv_from_gcp()
            self.split_data()

            logger.info("Data Ingestion completed Successfully")
        except Custom_exception as ce:
            logger.error(f"CustomException :{str(ce)}")
        finally:
            logger.info("Data Ingestion Completed")


if __name__ == "__main__":

    data_ingestion = DataIngestion(read_yaml(CONFIG_PATH))
    data_ingestion.run()
