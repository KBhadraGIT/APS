#Importing required dependencies
from typing import Optional
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler, LabelEncoder
import sys
from imblearn.combine import SMOTETomek
#===========================================================
from src.logger import logging
from src.exception import APSException
from src.entity import config_entity, artifact_entity
from src.config import TARGET_COLUMN
from src import utils




class DataTransformation:

    def __init__(self,
                 data_transformation_config: config_entity.DataTransformationConfig,
                 data_ingestion_artifact: artifact_entity.DataIngestionArtifact,):
        try:
            logging.info(f"{'>>'*20} DATA TRANSFORMATION {'<<'*20}")
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact

        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)
        

    @classmethod
    def get_data_transformer_object(cls) -> Pipeline:
        try:
            logging.info("Creating an instance for SimpleImputer")
            simple_imputer = SimpleImputer(strategy ='constant',
                                           fill_value = 0)
            logging.info("Creating an instance for RobustScaler")
            robust_scaler = RobustScaler()
            logging.info("Creating instance of Pipeline following the sequence: 1. Imputing 0 in case of missing values 2. Applying robust scaler on the dataset")
            pipeline = Pipeline(
                steps=[
                ('Imputer', simple_imputer),
                ('RobustScaler', robust_scaler)
                ]
            )

        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)


    def initiate_data_transformation(self,) -> artifact_entity.DataTransformationArtifact:
        try:
            #Loading datasets
            logging.info("Loading train dataset")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info("Loading test dataset")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)

            #Preparing train dataset and test dataset containing input features only
            logging.info("Dropping Target column from train dataset.")
            input_feature_train_df = train_df.drop(TARGET_COLUMN,axis=1)
            logging.info("Dropping Target column from test dataset.")
            input_feature_test_df = test_df.drop(TARGET_COLUMN,axis=1)

            #Preparing train dataset and test dataset containing only target column
            logging.info("Creating object of target column from train dataset")
            target_feature_train_df = train_df[TARGET_COLUMN]
            logging.info("Creating object of target column from test dataset")
            target_feature_test_df = test_df[TARGET_COLUMN]

            #Label encoding target column
            logging.info("Creating instance of label encoder.")
            label_encoder = LabelEncoder()
            logging.info("Fitting label encoder")
            label_encoder.fit(target_feature_train_df)
            logging.info("Applying label encoder on target objects.")
            target_feature_train_df = label_encoder.transform(target_feature_train_df)
            target_feature_test_df  = label_encoder.transform(target_feature_test_df)

            #Transformation pipeline
            logging.info("Creating instance of transformation pipeline.")
            transformation_pipeline = DataTransformation.get_data_transformer_object()
            logging.info("Fitting transformation_pipeline")
            logging.info("Applying transformation_pipeline on input_feature objects.")
            input_feature_train_df = transformation_pipeline.transform(input_feature_train_df)
            input_feature_test_df  = transformation_pipeline.transform(input_feature_test_df)

            #SMOTETomek
            logging.info("Creating instance of SMOTEK.")
            smt = SMOTETomek(random_state=config_entity.RANDOM_STATE)
            logging.info("Applying SMOTETomek on training dataset.")
            logging.info(f"Before applying SMOTETomek on training dataset shape of || Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr.shape}")
            input_feature_train_arr, target_feature_train_arr = smt.fit_resample(input_feature_train_arr, target_feature_train_arr)
            logging.info(f"After applying SMOTETomek on training dataset shape of || Input: {input_feature_train_arr.shape} Target:{target_feature_train_arr.shape}")
            logging.info("Applying SMOTETomek on testing dataset.")
            logging.info(f"Before applying SMOTETomek on testing dataset shape of || Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")
            input_feature_test_arr, target_feature_test_arr = smt.fit_resample(input_feature_test_arr, target_feature_test_arr)
            logging.info(f"After applying SMOTETomek on testing dataset shape of || Input: {input_feature_test_arr.shape} Target:{target_feature_test_arr.shape}")

            #Concatenating input feature and target column for both train and test dataset.
            logging.info("Concatenating the input feature and target column to prepare training dataset.")
            train_arr = np.c_[
                input_feature_train_arr,
                target_feature_train_arr
            ]
            logging.info("Concatenating the input feature and target column to prepare testing dataset.")
            test_arr = np.c_[
                input_feature_test_arr,
                target_feature_test_arr
            ]

            #Saving above datasets in NumPy.array format
            logging.info("Saving train dataset as NumPy.array format")
            utils.save_numpy_array_data(file_path = self.data_transformation_config.transformed_train_path,
                                        array = train_arr)
            logging.info("Saving test dataset as NumPy.array format")
            utils.save_numpy_array_data(file_path = self.data_transformation_config.transformed_train_path,
                                        array = train_arr)

            #saving the created instances as object as per requirements
            logging.info("Saving transformation_pipeline as an object.")
            utils.save_object(file_path = self.data_transformation_config.transform_object_path,
                              obj = transformation_pipeline) 
            logging.info("Saving label_encoder as an object.")
            utils.save_object(file_path = self.data_transformation_config.target_encoder_path,
                              obj = label_encoder)
            
            #Creating artifact of Data Transformation
            logging.info("Creating Data Transformation artifact.")
            data_transformation_artifact = artifact_entity.DataTransformationArtifact(
                transform_object_path = self.data_transformation_config.transform_object_path,
                target_encoder_path = self.data_transformation_config.target_encoder_path,
                transformed_train_path = self.data_transformation_config.transformed_train_path,
                transformed_test_path = self.data_transformation_config.transformed_test_path,
            )
            logging.info(f"Data transformation object {data_transformation_artifact}")

            return data_transformation_artifact


        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)

