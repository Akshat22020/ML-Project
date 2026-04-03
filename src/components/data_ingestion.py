# ============================
# DATA INGESTION MODULE
# ============================

# Reading the data.
# Data ingestion means collecting data from different sources (CSV, database, APIs, etc.)
# and making it ready for further processing in ML pipelines.

import os   # Used for interacting with the operating system (paths, folders, etc.)
import sys  # Provides access to system-specific parameters and functions

from src.exception import CustomException   # Custom exception handling (your own error class)
from src.logger import logging             # Custom logging module for tracking execution

import pandas as pd  # Used for handling datasets (DataFrames)

from sklearn.model_selection import train_test_split  # Used to split dataset into train & test

from dataclasses import dataclass  
# dataclass is used to automatically create init, repr, etc. for classes
# It is useful for storing configuration variables cleanly


# ============================
# CONFIGURATION CLASS
# ============================

@dataclass  
# This decorator automatically creates __init__ method
# So we don't need to manually define constructor
class DataIngestionConfig:
    
    # Path where training data will be stored
    train_data_path: str = os.path.join('artifacts', "train.csv")
    
    # Path where testing data will be stored
    test_data_path: str = os.path.join('artifacts', "test.csv")
    
    # Path where raw (original) data will be stored
    raw_data_path: str = os.path.join('artifacts', "data.csv")


# ============================
# MAIN DATA INGESTION CLASS
# ============================

class DataIngestion:
    
    def __init__(self):
        # Creating an object of config class
        # This allows us to access file paths easily
        self.ingestion_config = DataIngestionConfig()
    

    # Main function that performs ingestion
    def initiate_data_ingestion(self):
        
        # Logging is used instead of print for better debugging & tracking
        logging.info("Entered the data ingestion method or component")
        
        try:
            # Reading CSV file into pandas DataFrame
            
            df = pd.read_csv('notebook\data\stud.csv')
            
            logging.info("Read the dataset as dataframe")
            

            # Create directory if it doesn't exist
            # os.path.dirname gets folder name from file path
            # exist_ok=True avoids error if folder already exists
            os.makedirs(
                os.path.dirname(self.ingestion_config.train_data_path),
                exist_ok=True
            )

            # Saving raw data (original dataset)
            # index=False → removes index column
            # header=True → keeps column names
            df.to_csv(
                self.ingestion_config.raw_data_path,
                index=False,
                header=True
            )

            logging.info("Train test split initiated")


            # Splitting dataset into training (80%) and testing (20%)
            # random_state ensures same split every time (important for reproducibility)
            train_set, test_set = train_test_split(
                df,
                test_size=0.2,
                random_state=42
            )


            # Saving training data
            train_set.to_csv(
                self.ingestion_config.train_data_path,
                index=False,
                header=True
            )

            # Saving testing data
            test_set.to_csv(
                self.ingestion_config.test_data_path,
                index=False,
                header=True
            )

            logging.info("Ingestion of the data is completed")


            # Returning file paths so next pipeline step can use them
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            # If any error occurs, it is passed to custom exception handler
            # sys helps in tracking exact file + line number
            raise CustomException(e, sys)
        
if __name__=="__main__":
    obj=DataIngestion()
    obj.initiate_data_ingestion()