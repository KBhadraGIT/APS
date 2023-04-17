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
        """
        DESCRIPTION:
        This function drops columns from a Pandas DataFrame df that contain 
        missing values above a specified threshold. It also logs information 
        about the process and updates a validation error dictionary.
        =======================================================================
        PARAMETERS: 
        df: Pandas DataFrame
        report_key_name: key of the dictionary type report
        =======================================================================
        RETURN: Pandas DataFrame with dropped columns which have more missing 
        values more thamn threshold value."""
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
        

    def is_required_columns_exist(self,
                                  base_df: pd.DataFrame,
                                  current_df: pd.DataFrame,
                                  report_key_name: str) -> bool:
        """
        DESCRIPTION:
        The function then tries to compare the columns of the base dataset 
        and the current dataset. If any columns are missing in the current 
        dataset as compared to the base dataset, it logs the missing columns 
        using the logging module and returns False. If all required columns 
        are present, it returns True.
        =========================================================================
        PARAMETERS:
        base_df: Pandas DataFrame representing the base dataset
        current_df: Pandas DataFrame representing the current dataset
        report_key_name: It is a string representing the name of the report 
        to be generated.
        =========================================================================
        RETURN: 
        The function returns a boolean value indicating whether the current 
        dataframe is having all the columns of base dataframe or not. """
        try:
            base_columns = base_df.columns
            current_columns = current_df.columns

            missing_columns = []

            for base_column in base_columns:
                if base_column not in current_columns:
                    logging.info(f"{base_column} is not available.")
                    missing_columns.append(base_column)
            
            if len(missing_columns)>0:
                self.validation_error[report_key_name] = missing_columns
                return False
            
            return True

        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)


    def data_drift(self,
                   base_df: pd.DataFrame,
                   current_df: pd.DataFrame,
                   report_key_name: str):
        """
        DESCRIPTION:
        this function seems to be performing a hypothesis test to 
        determine if there is significant data drift between the 
        two datasets and updating a report with the results of this analysis.
        ==============================================================================
        PARAMETERS:
        base_df: Pandas DataFrame representing the base dataset
        current_df: Pandas DataFrame representing the current dataset
        report_key_name: Name of the report to be generated
        ==============================================================================
        RETURN: 
        This function will return the report with the results of this analysis.
        """
        try:
            drift_report = dict()
            base_columns = base_df.columns
            current_columns = current_df.columns

            for base_column in base_columns:
                base_data, current_data = base_df[base_column], current_df[base_column]
                logging.info(f"Hypothesis -> {base_column} [ {base_data.dtype} || {current_data.dtype} ]")
                logging.info("Our null hypthesis is the specific column will be having same distribution for both the dataset.")
                same_distribution = ks_2samp(base_data, current_data)

                if same_distribution.pvalue > 0.05:
                    logging.info("Accepting null hypothesis.")
                    drift_report[base_column] = {
                        "pvalues": float(same_distribution.pvalue),
                        "Same_distribution": True
                    }
                else:
                    logging.info("Rejecting null hypothesis.")
                    drift_report[base_column] = {
                        "pvalues": float(same_distribution.pvalue),
                        "Same_distribution": True
                    }

                self.validation_error[report_key_name] = drift_report

        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e,sys)


    def initiate_data_validation(self) -> artifact_entity.DataValidationArtifact:
        try:
            logging.info("Loading dataframes: Base DataFrame, Train DataFrame, Test DataFrame")
            base_df = pd.read_csv(self.data_validation_config.base)
            logging.info("Loaded Base DataFrame")
            train_df = pd.read_csv(self.data_ingestion_artifact.train_file_path)
            logging.info("Loaded Train DataFrame")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            logging.info("Loaded Test DataFrame")
            
            logging.info("replacing any 'na' values with np.NAN values in base_df.")
            base_df.replace({"na":np.NAN}, inplace = True)
            
            #Dropping columns having missing values more than threshold value.
            #Base DataFrame
            logging.info("Checking for missing values column wise and dropping the columns having execcessive missing values in base dataset.")
            base_df = self.drop_missing_values_column(df = base_df, 
                                                      report_key_name = "missing_values_within_base_dataset")
            #Train DataFrame
            logging.info("Checking for missing values column wise and dropping the columns having execcessive missing values in train dataset.")
            base_df = self.drop_missing_values_column(df = train_df, 
                                                      report_key_name = "missing_values_within_train_dataset")
            #Test DataFrame
            logging.info("Checking for missing values column wise and dropping the columns having execcessive missing values in test dataset.")
            base_df = self.drop_missing_values_column(df = test_df, 
                                                      report_key_name = "missing_values_within_test_dataset")         
            
            #Converting the data type of each and every columns of Base DataFrame, Train DataFrame and Test DataFrame
            #into float type except the excluded column.
            #Excluding column declared
            exclude_columns = [TARGET_COLUMN]
            logging.info("Converting the columns of Base DataFrame into float type.")
            base_df = utils.convert_columns_float(df=base_df, exclude_columns=exclude_columns)
            logging.info("Converting the columns of Train DataFrame into float type.")
            train_df = utils.convert_columns_float(df=train_df, exclude_columns=exclude_columns)
            logging.info("Converting the columns of Test DataFrame into float type.")
            test_df = utils.convert_columns_float(df=test_df, exclude_columns=exclude_columns)

            #Validating the columns in base dataframe, train dataframe and test dataframe:
            logging.info(f"Validating columns in train dataframe.")
            train_df_columns_status = self.is_required_columns_exists(base_df=base_df,
                                                                      current_df=train_df,
                                                                      report_key_name="missing_columns_within_train_dataset")
            logging.info(f"Validating columns in test dataframe.")
            test_df_columns_status = self.is_required_columns_exists(base_df=base_df,
                                                                     current_df=test_df,
                                                                     report_key_name="missing_columns_within_test_dataset")
            
            #Writing the report of the hypothesis testing
            logging.info("Writing report in yaml file.")
            


        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)  