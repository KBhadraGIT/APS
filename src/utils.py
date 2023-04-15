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
        raise APSException(e, sys)