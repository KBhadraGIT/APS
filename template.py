from pathlib import Path
import os, logging

logging.basicConfig(
    level=logging.INFO,
    format='[ %(asctime)s || %(levelname)s || %(message)s ]'
)


list_of_files = [
    "src/__init__.py",
    "src/components/__init__.py",
    "src/components/data_ingestion.py",
    "src/components/data_validation.py",
    "src/components/data_transformation.py",
    "src/components/model_trainer.py",
    "src/components/model_evaluation.py",
    "src/components/model_pusher.py",
    "src/entity/__init__.py",
    "src/entity/config_entity.py",
    "src/entity/artifact_entity.py",
    "src/pipeline/__init__.py",
    "src/logger.py",
    "src/exception.py",
    "src/utils.py",
    "requirements.txt",
    "setup.py"
]



for filepath in list_of_files:
    
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir != "":
        os.makedirs(filedir,exist_ok=True)
        logging.info(f"Creating a directory: {filedir} for file: {filename}")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
            logging.info(f"Creating file: {filepath}")

    else:
        logging.info(f"File already present: {filename}")