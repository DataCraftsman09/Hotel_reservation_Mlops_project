import os
import pandas as pd
import numpy as np
from src.logger import get_logger
from config.paths_config import *
from imblearn.over_sampling import SMOTE
from src.custom_exception import Custom_exception
from utils.common_functions import read_yaml,Load_data
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self, train_path, test_path, processed_dir,config_path):
        self.train_path = train_path
        self.test_path = test_path
        self.processed_dir = processed_dir
        
        self.config = read_yaml(config_path)

        if not os.path.exists(self.processed_dir):
            os.makedirs(self.processed_dir)
    
    def preprocess_data(self,df):
        try:
            logger.info("Starting the data preprocessing step")

            logger.info("Dropping the columns")
            df.drop(columns=["Unnamed: 0","Booking_ID"], inplace=True)

            df.drop_duplicates(inplace=True)

            cat_cols = self.config["data_processing"]["categorical_cols"]
            num_cols = self.config["data_processing"]["numerical_cols"]

            from sklearn.preprocessing import LabelEncoder

            LE = LabelEncoder()
            mappings = {}
            for cat_features in cat_cols:
                        df[cat_features] = LE.fit_transform(df[cat_features])
                        mappings[cat_features] = {label:code for label,code in zip(LE.classes_ , LE.transform(LE.classes_))}
        
            logger.info("Label Mappings are :")
            for col , mappings in mappings.items():
                logger.info(f"{col} : {mappings}")
        
            logger.info("Skewness handling....")

            skew_threshold = self.config["data_processing"]["skewness_threshold"]
            skewness =df[num_cols].apply(lambda x:x.skew())

            for col in skewness[skewness > skew_threshold].index:
                df[col] = np.log1p(df[col])
        
            return df
        
        except Exception as e:
             logger.error(f"Error during preprocess step {e}")
             raise Custom_exception("Error While preprocessing data",e)
    

    def balance_data(self, df):
         try:
              
            logger.info("Handling Imbalanced data")
            X = df.drop("booking_status",axis=1)
            y = df["booking_status"]

            smote = SMOTE(random_state=42)

            X_res , y_res = smote.fit_resample(X, y)

            balanced_df = pd.DataFrame(X_res,columns=X.columns)
            balanced_df["booking_status"] = y_res

            logger.info("Data balanced Successfully")

            return balanced_df
         
         except Exception as e:
             logger.error(f"Error during Balancing data step {e}")
             raise Custom_exception("Error While Balancing data",e)
         


    def select_features(self,df):
         try:
              logger.info("Starting our features selections Step")
              
              X = df.drop("booking_status",axis=1)
              y = df["booking_status"]

              model = RandomForestClassifier(random_state=42)

              model.fit(X,y)

              feature_importance = model.feature_importances_

              feature_importance_df = pd.DataFrame({
                    "feature" : X.columns,
                    "Importance":feature_importance
                    })
              
              top_features_df = feature_importance_df.sort_values(by="Importance", ascending=False)

              num_features =self.config["data_processing"]["no_of_features"]

              top_10_features = top_features_df["feature"].head(num_features).values
              
              logger.info(f"Features selected : {top_10_features}")
              top_10_df = df[top_10_features.tolist() + ["booking_status"]]

              logger.info("Feature selected successfully")

              return top_10_df
         except Exception as e:
             logger.error(f"Error during Feature Selection step {e}")
             raise Custom_exception("Error While Feature Selection ",e)
         

    def save_data(self,df, file_path):
         try:
              logger.info("saving our data in proccessed folder")

              df.to_csv(file_path, index=False)

              logger.info(f"data saved successfully to {file_path}")
         except Exception as e:
             logger.error(f"Error during Saving data step {e}")
             raise Custom_exception("Error While Saving data ",e)


    def process(self):
         try:

            logger.info("Loading the data from raw directory")

            train_df = Load_data(self.train_path) 
            test_df = Load_data(self.test_path)

            train_df = self.preprocess_data(train_df)
            test_df = self.preprocess_data(test_df)

            train_df = self.balance_data(train_df)
            test_df =self.balance_data(test_df)

            train_df = self.select_features(train_df)
            test_df = test_df[train_df.columns]

            self.save_data(train_df,PROCESSED_TRAIN_DATA_PATH)
            self.save_data(test_df,PROCESSED_TEST_DATA_PATH)

            logger.info("Data preprocessing completed successfully")
         except Exception as e:
             logger.error(f"Error during Data Preprocessing step {e}")
             raise Custom_exception("Error While Data Preprocessing pipeline",e)

              
if __name__ == "__main__":
     processor = DataProcessor(train_path=TRAIN_FILE_PATH,test_path=TEST_FILE_PATH,processed_dir=PROCESSED_DIR,config_path=CONFIG_PATH)
     processor.process()
          
              
              
              
              
              
             

         


    