from pathlib import Path
import os, logging

logging.basicConfig(
    level=logging.INFO,
    format='[ %(asctime)s || %(levelname)s || %(message)s ]'
)

while True:
    PROJECT = input("Enter the name of the project: ")
    if PROJECT != "":
        break

logging.info(f"Creating new project: {PROJECT}")

logging.info("Creating list of files present in the project {PROJECT}")

list_of_files = [
    f"src/__init__.py",
    f"src/components/__init__.py",
    f"src/components/data_ingestion.py",
    f"src/components/data_validation.py",
    f"src/components/data_transformation.py",
    f"src/components/model_trainer.py",
    f"src/components/model_evaluation.py",
    f"src/components/model_pusher.py",
    f"src/entity/__init__.py",
    f"src/entity/config_entity.py",
    f"src/entity/artifact_entity.py",
    f"src/pipeline/__init__.py",
    f"src/logger.py",
    f"src/exception.py",
    f"src/utils.py",
    f"requirements.txt",
    f"setup.py"
]

logging.info("Creating files in respective directories for the project {PROJECT}")

for file_path in list_of_files:
    logging.info("Here replacing all the '/' by '\'.")
    file_path = Path(file_path)
    logging.info("Separting directory and file name.")
    file_dir, file_name = os.path.split(file_path)

    if file_dir != '':
        os.makedirs(file_dir, exist_ok= True)
        logging.info(f"Creating directory: {file_dir}")

    if (not os.path.exists(file_dir)) or (os.path.getsize(file_dir) == 0):
        with open(file_path, 'w') as f:
            pass
        logging.info(f"Created file: {file_name} in directory: {file_path} ")

    else:
        logging.info(f'File already present in the directory.') 