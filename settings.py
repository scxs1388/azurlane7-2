import sys
import os

# mode
RECORD_ITEM = False

# path 
PATH = {
    "root_dir": sys.path[0],
    "data_dir": os.path.join(sys.path[0], "data"),
    "image_dir": os.path.join(sys.path[0], "image"),
    "temp_image_dir": os.path.join(sys.path[0], "image", "temp"),
    "commit_image_dir": os.path.join(sys.path[0], "image", "commit_image"),
    "submit_image_dir": os.path.join(sys.path[0], "image", "submit_image"),
    "sample_image_dir": os.path.join(sys.path[0], "image", "sample_image"),
    "commit_data_file_path": os.path.join(sys.path[0], "data", "commit_data.csv"),
    "submit_data_file_path": os.path.join(sys.path[0], "data", "submit_data.csv")
}

# commit_data.py
COMMIT_DATA_SETTINGS = {
    "client_info_file_path": os.path.join(PATH["root_dir"], "baidu_ai_client_info.txt"),
    "client_id": "",
    "client_secret": "",
    "user": "VirtualRiot"
}

# submit_data.py
SUBMIT_DATA_SETTINGS = {
    "submit_url": "https://www.scxs-studio.com/p/7-2/submit.php",
    "submit_info_file_path": os.path.join(PATH["root_dir"], "submit_info.txt"),
    "verify_code": "",
    "host": "",
    "user": "",
    "password": "",
    "database": ""
}

# standard data_dict
STANDARD_COMMIT_DATA_DICT = {
    "user": "",
    "datetime": 0,
    "oxycola": 0,
    "coolant": 0,
    "tempura": 0,
    "repair": 0,
    "ammo": 0,
    "klxd1": 0,
    "klxd2": 0,
    "klxd3": 0,
    "wsk1": 0,
    "wsk2": 0,
    "wsk3": 0,
    "zwzg1": 0,
    "zwzg2": 0,
    "zwzg3": 0,
    "blk1": 0,
    "blk2": 0,
    "blk3": 0,
    "coin1": 0,
    "coin2": 0,
    "coin3": 0,
    "coin4": 0,
    "j113": 0,
    "checked": True,
    "folder": 0
}