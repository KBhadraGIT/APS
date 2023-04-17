#Import required dependencies
from scipy.stats import ks_2samp
from typing import Optional
import os, sys
import pandas as pd
import numpy as np
#=============================================================
from src.logger import logging
from src.exception import APSException
from src import utils
from src.config import TARGET_COLUMN
from src.entity import artifact_entity, config_entity


class DataValidaton:


    def __init__(self,
                 data_validation_config: config_entity.DataValidationConfig,
                 data_ingestion_artifact: artifact_entity.DataIngestionArtifact):
        try:
            logging.info(f"{'>>'*20} Data Validation {'<<'*20}")
            self.data_validation_config = data_validation_config
            self.data_ingestion_artifact = data_ingestion_artifact
            self.validation_error = dict()

        except Exception as e:
            logging.error(APSException(e, sys))


    def drop_missing_values_column(self,
                                   df: pd.DataFrame,
                                   report_key_name: str) -> Optional[pd.DataFrame]:
        try:
            logging.info("Calculating the percentage of missing values for each column in the DataFrame df.")
            null_report = df.isna().sum/df.shape[0]

            threshold = self.data_validation_config.missing_threshold
            logging.info(f"Threshold limit for missing values for every column: {threshold}")

            logging.info(f"Selecting column name containing null values more than the threshold limit.")
            drop_column_names = null_report[ null_report > threshold ].index
            list_drop_column_names = list(drop_column_names)
            logging.info(f"Columns containg missing values more than threshold limit: {list_drop_column_names}")
            self.validation_error[report_key_name] = list_drop_column_names

            logging.info(f"Dropping the above columns from the dataframe")
            df.drop(list_drop_column_names,
                    axis=1,
                    inplace= True)
            #Condition if all the columns are removed 
            if len(df.columns) == 0:
                logging.info(f"Returned dataframe is empty.")
                return None
            return df
        
        except Exception as e:
            logging.error(APSException(e,sys))
            raise APSException(e,sys)
        
        

    def initiate_data_validation(self) -> artifact_entity.DataValidationArtifact:
        try:
            logging.info("Loading dataframe.")
            base_df = pd.read_csv(self.data_validation_config.base)
            logging.info("replacing any 'na' values with np.NAN values in base_df.")
            base_df.replace({"na":np.NAN}, inplace = True)


        except Exception as e:
            logging.error(APSException(e, sys))

