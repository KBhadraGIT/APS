#Importing libraries and dependencies
import os, sys
from datetime import datetime
#=============================================================
from src.exception import APSException
from src.logger import logging


#Declaring variables
FILE_NAME = "sensor.csv"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"
TEST_SIZE = 0.2
RANDOM_STATE = 42
MISSING_THRESHOLD = 0.2
TRANSFORMER_OBJECT_FILE_NAME = "transformer.pkl"
TARGET_ENCODER_OBJECT_FILE_NAME = "target_encoder.pkl"
MODEL_FILE_NAME = "model.pkl"
OVERFITTING_THRESHOLD = 0.1
EXPECTED_SCORE = 0.7
CHANGE_THRESHOLD = 0.1


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
        

class DataValidationConfig:

    def __init__(self,
                 training_pipeline_config:TrainingPipelineConfig,):
        
        #Using the TrainingPipelineConfig creating directory:  artifact/__timestamp__/data_validation
        self.data_validation_dir = os.path.join(training_pipeline_config.artifact_dir , "data_validation")

        #In data_validation directory report.yaml file is created that will contain the report generated during data validation
        self.report_file_path = os.path.join(self.data_validation_dir, "report.yaml")

        #Threshold limit for data validation stage
        self.missing_threshold:float = MISSING_THRESHOLD

        #Stored file for validation in .csv format
        self.base_file_path = self.base_file_path = os.path.join("aps_failure_training_set1.csv")


class DataTransformationConfig:

    def __init__(self,
                 training_pipeline_config:TrainingPipelineConfig,):
        #Using the TrainingPipelineConfig creating directory:  artifact/__timestamp__/data_transformation
        self.data_transformation_dir = os.path.join(training_pipeline_config.artifact_dir , "data_transformation")
        
        #In data transformation directiory a folder is created transformer, inside that transformer.pkl is created to store the transformer object.
        self.transform_object_path = os.path.join(self.data_transformation_dir,"transformer",TRANSFORMER_OBJECT_FILE_NAME)

        #In data transformation directiory a folder is created transformed, inside that train dataset is stored in .npz format after transformation.
        self.transformed_train_path =  os.path.join(self.data_transformation_dir,"transformed",TRAIN_FILE_NAME.replace("csv","npz"))

        #In data transformation directiory a folder is created transformed, inside that test dataset is stored in .npz format  after transformation.
        self.transformed_test_path =os.path.join(self.data_transformation_dir,"transformed",TEST_FILE_NAME.replace("csv","npz"))

        #In data transformation directiory a folder is created target_encoder, inside that target_encoder is stored in .pkl format  after transformation.
        self.target_encoder_path = os.path.join(self.data_transformation_dir,"target_encoder",TARGET_ENCODER_OBJECT_FILE_NAME)


class ModelTrainerConfig:

    def __init__(self,
                 training_pipeline_config: TrainingPipelineConfig,):
        #Using the TrainingPipelineConfig creating directory:  artifact/__timestamp__/model_trainer
        self.model_trainer_dir = os.path.join(training_pipeline_config.artifact_dir, "model_trainer")

        #Inside the above directory a folder is created "model" that will contain the trained model by name model.pkl
        self.model_path = os.path.join(self.model_trainer_dir, "model", MODEL_FILE_NAME)

        #Threshold value to check for overfitting and underfitting of the model
        self.overiftting_threshold = OVERFITTING_THRESHOLD
        self.expected_score = EXPECTED_SCORE


class ModelEvaluationConfig:

    def __init__(self, 
                 training_pipeline_config: TrainingPipelineConfig,):
        #Setting up threshold value for model evaluation
        self.change_threshold = CHANGE_THRESHOLD
