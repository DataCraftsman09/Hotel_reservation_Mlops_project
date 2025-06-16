import pandas as pd
import os
import lightgbm as lgb
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.logger import get_logger
from src.custom_exception import Custom_exception
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, Load_data
from scipy.stats import randint
import joblib

import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining:
    def __init__(self, train_path , test_path, model_ouput_path):
        self.train_path = train_path
        self.test_path = test_path
        self.model_ouput_path = model_ouput_path

        self.param_dist = LIGHTGBM_PARAM
        self.random_Search_params = RANDOM_SEARCH_PARAM

    def load_and_split_data(self):
        try:
            logger.info(f"Loading data From {self.train_path}")
            train_df = Load_data(self.train_path)

            logger.info(f"Loading data from {self.test_path}")
            test_df = Load_data(self.test_path)

            X_train  = train_df.drop("booking_status",axis=1)
            y_train = train_df["booking_status"]

            X_test = test_df.drop("booking_status",axis=1)
            y_test = test_df["booking_status"]

            logger.info("Data splitted successfully for Model training")

            return X_train, y_train , X_test, y_test
        except Exception as e:
            logger.error(f"Error While splitting the data {e}")
            raise Custom_exception("Failed to load the data",e)
            
    def train_lgbm(self, X_train , y_train):
        try:
            logger.info("Initializing our model")

            lgbm_model =  lgb.LGBMClassifier(random_state=self.random_Search_params["random_state"])
            
            logger.info("Starting hyperparameter tuning")

            random_search = RandomizedSearchCV(
                estimator=lgbm_model,
                param_distributions=self.param_dist,
                n_iter=self.random_Search_params["n_iter"],
                cv = self.random_Search_params["cv"],
                verbose=self.random_Search_params["verbose"],
                random_state=self.random_Search_params["random_state"],
                n_jobs=self.random_Search_params["n_jobs"],
                scoring=self.random_Search_params["scoring"]
            )

            logger.info("starting our Hyperparameter tuning")

            random_search.fit(X_train,y_train)

            logger.info("Hyperparameter tuning completed")

            best_params = random_search.best_params_
            best_lgbm_model = random_search.best_estimator_

            logger.info(f"Best parameters are : {best_params}")

            return best_lgbm_model
        
        except Exception as e:
            logger.error(f"Error While Training data {e}")
            raise Custom_exception("Failed to train data",e)
        
    
    def evaluate_model(self,model , X_test, y_test):
        try:
            logger.info("Evaluating the model")

            y_preds = model.predict(X_test)

            accuracy = accuracy_score(y_test,y_preds)
            precision = precision_score(y_test,y_preds)
            recall = recall_score(y_test, y_preds)
            f1 = f1_score(y_test,y_preds)

            logger.info(f"Accuracy_score:{accuracy}")
            logger.info(f"Precision Score: {precision}")
            logger.info(f"recall_score:{recall}")
            logger.info(f"f1_score:{f1}")

            return {
                "Accuracy_score" : accuracy,
                "Precision": precision,
                "recall": recall,
                "F1-score":  f1
            }
        
        except Exception as e:
            logger.error(f"Error While Evaluating Model {e}")
            raise Custom_exception("Failed to Evaluate Model",e)
        

    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_ouput_path),exist_ok=True)

            logger.info("Saving the model")

            joblib.dump(model,self.model_ouput_path)

            logger.info(f"saved the model successfully to {self.model_ouput_path}")

        except Exception as e:
            logger.error(f"Error While saving the model {e}")
            raise Custom_exception("Failed to save Model",e)
    
    def run(self):
        try:
            with mlflow.start_run():

                logger.info("Starting our model training pipeline")

                logger.info("Starting our Mlflow experimentation")

                logger.info("Logging the training and testing dataset to Mlflow")
                mlflow.log_artifact(self.train_path, artifact_path="datasets")

                mlflow.log_artifact(self.test_path , artifact_path="datasets")

                X_train, y_train , X_test, y_test = self.load_and_split_data()

                best_lgbm_model = self.train_lgbm(X_train,y_train)

                eval_metrics = self.evaluate_model(best_lgbm_model,X_test,y_test)

                self.save_model(best_lgbm_model)

                logger.info("Logging the model into MLflow")
                mlflow.log_artifact(self.model_ouput_path)

                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(eval_metrics)

                logger.info("Model training successful")

        except Exception as e:
            logger.error(f"Error While model training pipeline {e}")
            raise Custom_exception("Failed during model training pipeline",e)

if __name__ == "__main__":
    trainer = ModelTraining(PROCESSED_TRAIN_DATA_PATH,PROCESSED_TEST_DATA_PATH,MODEL_OUPUT_PATH)
    trainer.run()


