import os
import shutil

PERSISTENT_PATH = "data/uploaded_data.xlsx"

def save_file(uploaded_file):
    with open(PERSISTENT_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())

def get_uploaded_file():
    return PERSISTENT_PATH if os.path.exists(PERSISTENT_PATH) else None
