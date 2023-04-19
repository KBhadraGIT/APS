#Importing required dependencies
from typing import Optional
import os,sys
from xgboost import XGBClassifier
#==================================================
from src.entity import config_entity, artifact_entity
from src.logger import logging
from src.exception import APSException


class ModelTrainer:

    def __init__(self,
                 model_trainer_config: config_entity.ModelTrainerConfig,
                 data_transformation_artifact: artifact_entity.DataTransformationArtifact,):
        try:
            logging.info(f"{'>>'*20} MODEL TRAINING {'<<'*20}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        
        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)


    def train_model(self, Input_feature, Target_feature):
        try:
            logging.info("Creating instance of XG-boost Classifier")
            xgb = logging.info('the is the test for the code')