#Importing required dependencies:
import sys
import pandas as pd
from sklearn.metrics import accuracy_score
#=============================================
from src.entity import config_entity, artifact_entity
from src.logger import logging
from src.exception import APSException
from src.latest_path import LatestPathFinder
from src.utils import load_object
from src.config import TARGET_COLUMN


class ModelEvaluation:

    def __init__(self,
                 model_evaluation_config : config_entity.ModelEvaluationConfig,
                 data_ingestion_artifact : artifact_entity.DataIngestionArtifact,
                 data_transformation_artifact : artifact_entity.DataTransformationArtifact,
                 model_trainer_artifact : artifact_entity.ModelTrainerArtifact):
        try:
            logging.info(f"{'>>'*20}  MODEL EVALUATION  {'<<'*20}")
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_artifact = data_transformation_artifact
            self.model_trainer_artifact = model_trainer_artifact
            self.model_evaluation_config = model_evaluation_config
            self.latest_path_finder = LatestPathFinder()
        
        except Exception as e:
            logging.error(APSException(e,sys))
            raise APSException(e,sys)
        
    
    def initiate_model_evaluation(self) -> artifact_entity.ModelEvaluationArtifact:

        try:
            #Comparing the existing model and newly trained model for our data
            logging.info("If save_model folder consists of any existing model then \
                        comparing the existing model and newly trained model for our data")
            latest_dir_path = self.latest_path_finder.get_latest_dir_path()
            if latest_dir_path == None:
                model_evaluation_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted = True,
                                                                                    improved_accuracy = None)
                logging.info(f"Model evaluation artifact: {model_evaluation_artifact}")
                return model_evaluation_artifact
            

            #Saved objects

            #Fetching location of latest saved objects: transformer, model and target encoder
            logging.info("Finding location of latest saved transformer object")
            transformer_path = self.latest_path_finder.get_latest_transformer_path()
            logging.info("Finding location of latest saved model object")
            model_path = self.latest_path_finder.get_latest_model_path()
            logging.info(
                "Finding location of latest saved target_encoder object")
            target_encoder_path = self.latest_path_finder.get_latest_target_encoder_path()

            #loading latest saved objects: transformer, model and target encoder
            logging.info("Loading latest saved transformer object")
            transformer = load_object(file_path = transformer_path)
            logging.info("Loading latest saved model object")
            model = load_object(file_path=model_path)
            logging.info("Loading latest saved target_encoder object")
            target_encoder = load_object(file_path = target_encoder_path)


            #Current objects

            #Loading current objects: transformer, model, target_encoder
            logging.info("Loading current object: transformer")
            current_transformer = load_object(file_path=self.data_transformation_artifact.transform_object_path)
            logging.info("Loading current object: model")
            current_model = load_object(file_path=self.model_trainer_artifact.model_path)
            logging.info("Loading current objects: target_encoder")
            current_target_encoder = load_object(file_path=self.data_transformation_artifact.target_encoder_path)

            #Loading testing dataset
            logging.info("Loading test dataframe.")
            test_df = pd.read_csv(self.data_ingestion_artifact.test_file_path)
            #preparing target column
            logging.info("Loading target feature of test dataframe.")
            target_df = test_df[TARGET_COLUMN]
            logging.info("Encoding target feature.")
            y_true = target_encoder.transformer(target_df)

            #Preparing input feature  dataset for latest saved objects
            logging.info("Extracting name of features used in transformation.")
            input_feature_name = list(transformer.feature_names_in_)
            logging.info("Loading the input features of dataset and transforming it to desired form.")
            input_arr = transformer.transform(test_df[input_feature_name])

            #Using the latest saved model to predict data
            y_pred = model.predict(input_arr)
            print(f"Prediction using latest saved model: {target_encoder.inverse_transform(y_pred[:5])}")
            saved_model_score = accuracy_score(y_true = y_true,
                                               y_pred = y_pred)
            logging.info(f"Accuracy using latest saved trained model: {saved_model_score}")
            
            #Preparing input feature  dataset for current objects
            logging.info("Extracting name of features used in transformation.")
            input_feature_name = list(current_transformer.feature_names_in_)
            logging.info("Loading the input features of dataset and transforming it to desired form.")
            input_arr = transformer.transform(test_df[input_feature_name])
            
            #Using the current model to predict data
            y_pred = current_model.predict(input_arr)
            y_true = current_target_encoder.transform(target_df)
            print(f"Prediction using latest saved model: {current_target_encoder.inverse_transform(y_pred[:5])}")
            current_model_score = accuracy_score(y_true=y_true,
                                                 y_pred=y_pred)
            logging.info(f"Accuracy using current trained model: {current_model_score}")

            logging.info(f"Accuracy scores: Latest saved model: {saved_model_score} || Current model: {current_model_score}")
            if current_model_score <= saved_model_score:
                logging.info(f"Current trained model is not better than previous model")
                raise Exception("Current trained model is not better than previous model")

            model_eval_artifact = artifact_entity.ModelEvaluationArtifact(is_model_accepted=True,
                                                                          improved_accuracy=current_model_score-saved_model_score)
            logging.info(f"Model eval artifact: {model_eval_artifact}")
            return model_eval_artifact

        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)
