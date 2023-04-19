#Importing required dependencies
from typing import Optional
import os,sys
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score
#==================================================
from src.entity import config_entity, artifact_entity
from src.logger import logging
from src.exception import APSException
from src import utils

class ModelTrainer:

    def __init__(self,
                 model_trainer_config: config_entity.ModelTrainerConfig,
                 data_transformation_artifact: artifact_entity.DataTransformationArtifact,):
        try:
            logging.info(f"{'>>'*20} MODEL TRAINING {'<<'*20}")
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artifact = data_transformation_artifact
        
        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)


    def train_model(self, input_feature_train, target_feature_train):
        try:
            logging.info("Creating instance of XG-boost Classifier")
            xgb_clf = XGBClassifier()
            xgb_clf.fit(input_feature_train, target_feature_train)
            return xgb_clf

        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)
            

    def initiate_model_trainer(self,) -> artifact_entity.ModelTrainerArtifact:
        try:
            #Loading Dataset
            logging.info("Loading training dataset")
            train_arr = utils.load_numpy_array_data(file_path= self.data_transformation_artifact.transformed_train_path)
            logging.info("Loading test dataset")
            test_arr = utils.load_numpy_array_data(file_path= self.data_transformation_artifact.transformed_test_path)

            #Splitting the dataset into input features and target column
            logging.info("Splitting training dataset into X_train, y_train")
            X_train, y_train = train_arr[ : , :-1], train_arr[ : , -1]
            logging.info("Splitting test dataset into X_test, y_test")
            X_test, y_test = test_arr[ : , :-1], test_arr[ : , -1]

            #Training the model
            logging.info("Training the model on training dataset")
            model = self.train_model(input_feature_train = X_train,
                                     target_feature_train = y_train)

            #Applying model prediction and evaluating scores
            #For training dataset
            logging.info("Applying model prediction on training dataset.")
            y_train_ped = model.predict(X_train)
            acc_train_score = accuracy_score(y_true = y_train,
                                             y_pred = y_train_ped)
            logging.info(f"Accuracy of model for training dataset: {acc_train_score}")
            f1_train_score = f1_score(y_true = y_train,
                                      y_pred = y_train_ped)
            logging.info(f"F1-score of model for training dataset: {f1_train_score}")
            #For test dataset
            logging.info("Applying model prediction on training dataset.")
            y_test_ped = model.predict(X_test)
            acc_test_score = accuracy_score(y_true = y_test,
                                             y_pred = y_test_ped)
            logging.info(f"Accuracy of model for training dataset: {acc_test_score}")
            f1_test_score = f1_score(y_true = y_test,
                                      y_pred = y_test_ped)
            logging.info(f"F1-score of model for test dataset: {f1_test_score}")

            #Checking if the model is either underfitting or overfitting
            logging.info("Checking if the model is underfitting or not")
            if f1_test_score < self.model_trainer_config.expected_score:
                logging.info(f"Trained model is not good, since its accuracy: {acc_test_score} is \
                             leaas than {self.model_trainer_config.expected_score}.")
                raise Exception(f"Trained model is not good, since its accuracy: {acc_test_score} is \
                                leaas than {self.model_trainer_config.expected_score}.")
            logging.info("Model is not underfitting.")

            logging.info("Checking for overfitting")
            if acc_test_score < acc_train_score:
                logging.info("Trained model is overfitting")
                raise Exception("Trained model is overfitting")
            logging.info("Model is not overfitting.")

            #saving the trained model
            logging.info("Saving the model as an object")
            utils.save_object(file_path = self.model_trainer_config.model_path,
                              obj = model)
            
            #Creating artifact for Model trainer
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(
                model_path = self.model_trainer_config.model_path,
                acc_train_score = acc_train_score,
                acc_test_score = acc_test_score,
                f1_train_score = f1_train_score,
                f1_test_score = f1_test_score)

            #Output of Model Trainer is ready
            return model_trainer_artifact
        
        except Exception as e:
            logging.error(APSException(e, sys))
            raise APSException(e, sys)