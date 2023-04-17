#Importing required dependencies
import pandas as pd
import numpy as np
import sys, os
from sklearn.model_selection import train_test_split
#=============================================================
from src.logger import logging
from src.exception import APSException
from src.entity import config_entity, artifact_entity
from src.utils import get_collection_as_dataframe


class DataIngestion:
    def __init__(self, 
                 data_ingestion_config : config_entity.DataIngestionConfig):
        try:
            logging.info(f"{'>>'*20} Data Ingestion {'<<'*20}")
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise APSException(e, sys)
        
    def initiate_data_ingestion(self) -> artifact_entity.DataIngestionArtifact:
        try:
            logging.info("Exporting the data collection as pandas' dataframe.")
            df:pd.DataFrame = get_collection_as_dataframe(
                database_name = self.data_ingestion_config.database_name,
                collection_name= self.data_ingestion_config.collection_name,
            )
            
            logging.info("Saving data in feature store folder.")

            logging.info("Replacing na with numpy's NAN i.e. numpy.NAN")
            df.replace(to_replace="na",value=np.NAN,inplace=True)

            logging.info("Creating a folder name feature_store if not exist.")
            feature_store_dir = os.path.dirname(self.data_ingestion_config.feature_store_file_path)
            os.makedirs(feature_store_dir, exist_ok= True)

            logging.info("Saving the DataFrame in freature_store folder")
            df.to_csv(path_or_buf=self.data_ingestion_config.feature_store_file_path,
                      index = False,
                      header = True,)
            
            logging.info(f"Split dataset into train and test dataset in ration: {1-self.data_ingestion_config.test_size}:{self.data_ingestion_config.test_size}.")
            train_df, test_df = train_test_split(df,
                                                 test_size=self.data_ingestion_config.test_size,
                                                 random_state=self.data_ingestion_config.random_state)
            
            logging.info("Creating directory folder with name dataset for train and test dataset if not exist.")
            dataset_dir = os.path.dirname(self.data_ingestion_config.train_file_path)
            os.makedirs(dataset_dir,exist_ok=True)

            logging.info("Converting the train DataFrame to .csv format and storing it in the directory: self.data_ingestion_config.train_file_path")
            train_df.to_csv(path_or_buf = self.data_ingestion_config.train_file_path, 
                            index = False, 
                            header = True)
            
            logging.info("Converting the test DataFrame to .csv format and storing it in the directory: self.data_ingestion_config.test_file_path")
            test_df.to_csv(path_or_buf = self.data_ingestion_config.test_file_path, 
                            index = False, 
                            header = True)

            #Following are the objects returned by Data Ingestion component: complete dataset, train dataset and test dataset
            data_ingestion_artifact = artifact_entity.DataIngestionArtifact(feature_store_file_path=self.data_ingestion_config.feature_store_file_path,
                                                                            train_file_path=self.data_ingestion_config.train_file_path,
                                                                            test_file_path=self.data_ingestion_config.test_file_path,)
            
            logging.info("File paths of the following objects are returned by Data Ingestion component: feature_store, train dataset and test dataset")
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        
        except Exception as e:
            logging.error(APSException(error_message=e, error_detail=sys))
            raise APSException(error_message=e, error_detail=sys)