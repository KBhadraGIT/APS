#Importing libraries and dependencies
import os, sys
from src.exception import APSException
from src.logger import logging
from datetime import datetime

#Declaring variables
FILE_NAME = "sensor.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TEST_SIZE = 0.2
RANDOM_STATE = 42


class TrainingPipelineConfig:
    """
    Description:
    Here, we are setting up the self.artifact_dir variable to a path string 
    that includes the current working directory, a folder named "artifact",
    and a timestamp formatted as year-month-day and hour-minute-second.

    Return:
    It will create a new directory for storing artifacts corresponding to the
    components of the pipeline, with the directory name indicating when the 
    artifacts were generated.
    """
    def __init__(self):
        try:
            self.artifact_dir = os.path.join(os.getcwd(), "artifact", f"{datetime.now().strftime('%Y%m%d__||__%H%M%S')}")
        except Exception as e:
            logging.error(APSException(e,sys))
            raise APSException(e,sys)


class DataIngestionConfig:

    def __init__(self,
                 training_pipeline_config:TrainingPipelineConfig,):
        
        try:
            self.database_name="aps"
            self.collection_name="sensor"
            
            #Using the TrainingPipelineConfig creating directory:  artifact/__timestamp__/data_ingestion
            self.data_ingestion_dir = os.path.join(training_pipeline_config.artifact_dir , "data_ingestion")
            
            #Creating directory {feature_store} containing {sensor.csv}
            self.feature_store_file_path = os.path.join(self.data_ingestion_dir,"feature_store",FILE_NAME)
            
            #Creating directory {dataset} containig {train.csv} || {test.csv}
            self.train_file_path = os.path.join(self.data_ingestion_dir,"dataset",TRAIN_FILE_NAME)
            self.test_file_path = os.path.join(self.data_ingestion_dir,"dataset",TEST_FILE_NAME)
            
            #Population count of test dataset
            self.test_size = TEST_SIZE
            self.random_state = RANDOM_STATE

        except Exception  as e:
            raise APSException(e,sys)     

    def to_dict(self,)->dict:
        try:
            return self.__dict__
        except Exception  as e:
            raise APSException(e,sys)
        

class DataValidationConfig:

    def __init__(self,
                 training_pipeline_config:TrainingPipelineConfig,):
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir , "data_validation")
        self.report_file_path=os.path.join(self.data_validation_dir, "report.yaml")
        self.missing_threshold:float = 0.2
        self.base_file_path = os.path.join("aps_failure_training_set1.csv")