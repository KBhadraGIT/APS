#Importing required dependencies
import os, sys
from glob import glob
from typing import Optional
#=======================================================
from src.logger import logging
from src.exception import APSException
from src.entity.config_entity import TRANSFORMER_OBJECT_FILE_NAME, MODEL_FILE_NAME, TARGET_ENCODER_OBJECT_FILE_NAME

class latest_path_finder:

    def __init__(self,
                 model_registry = "saved_models",
                 transformer_dir_name = "transformer",
                 target_encoder_dir_name = "target_encoder",
                 model_dir_name = "model"):
        try:
            self.model_registry = model_registry
            #Creating directory to save models
            os.makedirs(self.model_registry, exist_ok= True)
            self.transformer_dir_name = transformer_dir_name
            self.target_encoder_dir_name = target_encoder_dir_name
            self.model_dir_name = model_dir_name

        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)
        

    def get_latest_dir_path(self) -> Optional[str]:
        """
        DESCRIPTION:
        This function will return None if there are no file present in 
        the model_registry folder. If there is any file present then it 
        converts the list of filenames from strings to integers using 
        the map function. This assumes that the filenames are integers.

        Then finds the maximum integer value in the list of filenames, 
        which corresponds to the latest directory.
        ================================================================
        RETURN: The path to the latest directory
        """
        try:
            dir_names = os.listdir(self.model_registry)
            if len(dir_names) == 0:
                return None
            #Converting the list of filenames from strings to integers
            dir_names = list(map(int, dir_names))
            latest_dir_name = max(dir_names)
            return os.path.join(self.model_registry, f"{latest_dir_name}")
            
        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)


    def get_latest_model_path(self):
        """
        DESCRIPTION:
        Return the path of the transformer object file in the latest 
        directory of the model registry.
        =============================================================
        RETURN:
        str: The path of the transformer object file in the latest 
        directory of the model registry.
        """
        try:
            latest_dir = self.get_latest_dir_path
            if latest_dir is None:
                raise Exception(f"Model is not available.")
            return os.path.join(latest_dir,
                                self.model_dir_name,
                                MODEL_FILE_NAME,)

        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)
        
    def get_latest_transformer_path(self):
        """
        DESCRIPTION:
        Return the path of the transformer object file in the 
        latest directory of the model registry.

        If the latest directory path is `None`, an `Exception` 
        is raised with the message "Transformer is not available".
        ==========================================================
        RETURNS:
        str: The path of the transformer object file in the latest 
        directory of the model registry.
        """
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Transformer is not available")
            return os.path.join(latest_dir, 
                                self.transformer_dir_name, 
                                TRANSFORMER_OBJECT_FILE_NAME,)
        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)


    def get_latest_target_encoder_path(self):
        """
        DESCRRIPTION:
        Return the path of the target encoder object file 
        in the latest directory of the model registry.

        If the latest directory path is `None`, an `Exception` 
        is raised with the message "Target encoder is not available".
        ===============================================================
        RETURNS:
        str: The path of the target encoder object file in the latest 
        directory of the latest directory of the model registry.
        """
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir is None:
                raise Exception(f"Target encoder is not available")
            return os.path.join(latest_dir, 
                                self.target_encoder_dir_name, 
                                TARGET_ENCODER_OBJECT_FILE_NAME,)
        
        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)
        

    def get_latest_save_dir_path(self) -> str:
        """
        DESCRIPTION:
        Return the path of the next directory in the model registry.
        If the latest directory path is `None`, the method returns a 
        path with the name "0" in the model registry. Otherwise, the 
        method increments the name of the latest directory in the 
        model registry by 1 and returns the path to the new directory.
        ==============================================================
        RETURN:
        str: The path of the next directory in the model registry.
        """
        try:
            latest_dir = self.get_latest_dir_path()
            if latest_dir == None:
                return os.path.join(self.model_registry, f"{0}")
            latest_dir_num = int(os.path.basename(self.get_latest_dir_path()))
            return os.path.join(self.model_registry, 
                                f"{latest_dir_num+1}")
        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)


    def get_latest_save_model_path(self):
        """
        DESCRIPTION:
        This function returns the path of the model file in 
        the latest save directory.
        ====================================================
        RETURN:
        str: The path of the model file in the latest save directory.
        """
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, 
                                self.model_dir_name, 
                                MODEL_FILE_NAME)
        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)


    def get_latest_save_transformer_path(self):
        """
        DESCRIPTION:
        This function returns the path of the transformer 
        object file in the latest save directory.
        ====================================================
        RETURN:
        str: The path of the transformer object file in the 
        latest save directory.
        """
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, 
                                self.transformer_dir_name, 
                                TRANSFORMER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e


    def get_latest_save_target_encoder_path(self):
        """
        DESCRIPTION:
        This function returns the path of the target encoder 
        object file in the latest save directory.
        ====================================================
        RETURN:
        str: The path of the target encoder object file in 
        the latest save directory.
        """
        try:
            latest_dir = self.get_latest_save_dir_path()
            return os.path.join(latest_dir, 
                                self.target_encoder_dir_name, 
                                TARGET_ENCODER_OBJECT_FILE_NAME)
        except Exception as e:
            raise e


