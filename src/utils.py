#Importing required dependencies
import pandas as pd
import sys


#Importing required components within the project
from src.logger import logging
from src.exception import APSException
from src.config import mongo_client


def get_collection_as_dataframe(database_name: str, collection_name: str) -> pd.DataFrame:
    """
    DESCRIPTION:
        This function reads data from MongoDB database and returns it as a pandas DataFrame.
    ====================================================================================
    PARAMETERS:
        database_name: database name
        collection_name: collection name
    ====================================================================================
    RETURN:
        Pandas dataframe of a collection
    """
    try:
        logging.info(f"Reading data from database: {database_name} and collection: {collection_name}")
        df = pd.DataFrame(list(mongo_client[database_name][collection_name].find()))
        logging.info(f"Found columns: {df.columns}")
        if "_id" in df.columns:
            logging.info(f"Dropping column: _id ")
            df = df.drop("_id",axis=1)
        logging.info(f"Row and columns in df: {df.shape}")
        return df
    
    except Exception as e:
        logging.error(APSException(e, sys))
        raise APSException(e, sys)
    

def convert_columns_float(df:pd.DataFrame,exclude_columns:list)->pd.DataFrame:
    """
    DESCRIPTION:
    This code converts all columns in a Pandas DataFrame df to the float data 
    type, except for those listed in exclude_columns.
    ==========================================================================
    PARAMETERS:
    df: pandas.DataFrame
    exclude_columns: Columns needed to be excluded
    ==========================================================================
    RETURN: Pandas DataFrame with columns of float data type.
    """
    try:
        for column in df.columns:
            if column not in exclude_columns:
                df[column]=df[column].astype('float')
        return df
    
    except Exception as e:
        logging.error(APSException(e, sys))
        raise APSException(e, sys) 