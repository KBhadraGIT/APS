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


    
    def initiate_data_validation(self) -> artifact_entity.DataValidationArtifact:
        try:
            logging.info("Loading dataframe.")
            base_df = pd.read_csv(self.data_validation_config.base)
            logging.info("replacing any 'na' values with np.NAN values in base_df.")
            base_df.replace({"na":np.NAN}, inplace = True)


        except Exception as e:
            logging.error(APSException(e, sys))

