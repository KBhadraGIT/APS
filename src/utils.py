#Importing required dependencies
import pandas as pd
import numpy as np
import sys,os
import yaml
import dill
#=========================================================================================
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
    

def convert_columns_float(df: pd.DataFrame, exclude_columns: list) -> pd.DataFrame:
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
    

def write_yaml_file(file_path, data: dict) -> None:
    """
    DESCRIPTION:
    This function will write the report of the analysis to a YAML file
    in dictionary format.
    ==========================================================================
    PARAMETERS:
    file_path: the path of the YAML file to be written to
    data: a dictionary containing the data to be written to the YAML file
    ==========================================================================
    RETURN: YAML file containing the report.
    """
    try:
        file_dir = os.path.dirname(file_path)
        os.makedirs(file_dir,exist_ok=True)
        with open(file_path,"w") as file_writer:
            yaml.dump(data,file_writer)
    
    except Exception as e:
        logging.error(APSException(e, sys))
        raise APSException(e, sys)
    

def save_numpy_array_data(file_path: str, array: np.array) -> None:
    """
    DESCRIPTION
    This function will write the data in NumPy.array form and 
    save it as an object file in the directory by creating a 
    directory path if it doesn't exist.
    =============================================================
    PARAMETERS
    file_path: Directory to save the file
    array: Format of dataset
    =============================================================
    RETURN: None
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        logging.error(APSException(e, sys))
        raise APSException(e, sys)
    

def save_object(file_path: str, obj: object) -> None:
    """
    DESCRIPTION:
    This function takes in a file path and an object as input, 
    and saves the object to the file specified by the file path.
    =============================================================
    PARAMETERS
    file_path: Directory to save the file
    array: Format of dataset
    =============================================================
    RETURN: None
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok= True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)

    except Exception as e:
        logging.error(APSException(e, sys))
        raise APSException(e, sys)
    

def load_numpy_array_data(file_path: str) -> np.array:
    """
    DESCRIPTION:
    This function will load numpy array data from the file 
    path and return a NumPy.array
    =======================================================
    PARAMETERS:
    file_path: location of file to be loaded in str format
    =======================================================
    RETURN: NumPy.array
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
        
    except Exception as e:
        logging.error(APSException(e, sys))
        raise APSException(e, sys)    
    

def save_object(file_path: str, obj: object):
    """
    DESCRIPTION:
    This function will intake the directory as string value 
    and store the object in the given directory.
    =======================================================
    PARAMETERS:
    file_path: location of file to be loaded in str format
    obj: object name to be saved
    =======================================================
    RETURN: None
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok= True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Object saved")
        
    except Exception as e:
        logging.error(APSException(e, sys))
        raise APSException(e, sys)
    

def load_object(file_path: str, ) -> object:
    """
    DESCRIPTION:
    This function will take the directory as a string value
    and return the object
    =======================================================
    PARAMETERS:
    file_path: location/directory of file to be loaded in
               str format
    =======================================================
    RETURN: object
    """
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} is not exists")
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
        
    except Exception as e:
        logging.error(APSException(e, sys))
        raise APSException(e, sys)
