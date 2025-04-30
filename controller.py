# controller.py
import os
from training.trainer import train_model

# Global variables
BASE_MODEL_PATH = None
DATASET_PATH = None

def set_base_model(path):
    global BASE_MODEL_PATH
    BASE_MODEL_PATH = path
    return BASE_MODEL_PATH

def set_dataset(path):
    global DATASET_PATH
    DATASET_PATH = path
    return DATASET_PATH

def clear_base_model():
    global BASE_MODEL_PATH
    BASE_MODEL_PATH = None

def clear_dataset():
    global DATASET_PATH
    DATASET_PATH = None

def start_training(update_console, epochs=1, batch_size=4, learning_rate=5e-4):
    if not BASE_MODEL_PATH or not DATASET_PATH:
        return False, "Please select both a base model and a dataset before starting training."

    try:
        train_model(
            BASE_MODEL_PATH,
            DATASET_PATH,
            progress_callback=update_console,
            epochs=epochs,
            batch_size=batch_size,
            learning_rate=learning_rate
        )
        return True, "Training completed successfully."
    except Exception as e:
        return False, f"Training failed: {str(e)}"