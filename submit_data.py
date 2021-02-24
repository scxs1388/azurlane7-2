import os
import shutil
import sys
import time
from datetime import datetime

import numpy as np
import pandas as pd
import pymysql
import requests
from tqdm import tqdm

from settings import PATH, SUBMIT_DATA_SETTINGS


def submit_data(data_code, verify_code):
    data = {
        "dataCode": data_code,
        "verifyCode": verify_code
    }
    res = requests.post(SUBMIT_DATA_SETTINGS["submit_url"], data=data)
    return res


def move_image():
    start_num = len(os.listdir(PATH["submit_image_dir"])) + 1
    for i, d in enumerate(os.listdir(PATH["commit_image_dir"])):
        shutil.move(os.path.join(PATH["commit_image_dir"], d), os.path.join(PATH["submit_image_dir"], str(start_num + i)))


def update_local_submit_data():
    submit_data_flie = pd.read_csv(PATH["submit_data_file_path"], encoding="GB2312")
    df = pd.DataFrame(submit_data_flie)
    if len(SUBMIT_DATA_SETTINGS["host"]) == 0:
        with open(SUBMIT_DATA_SETTINGS["submit_info_file_path"], encoding="utf-8") as file:
            data = file.readlines()
            SUBMIT_DATA_SETTINGS["verify_code"] = data[0][:-1]
            SUBMIT_DATA_SETTINGS["host"] = data[1][:-1]
            SUBMIT_DATA_SETTINGS["user"] = data[2][:-1]
            SUBMIT_DATA_SETTINGS["password"] = data[3][:-1]
            SUBMIT_DATA_SETTINGS["database"] = data[4][:-1]
    conn = pymysql.connect(
        host=SUBMIT_DATA_SETTINGS["host"],
        user=SUBMIT_DATA_SETTINGS["user"],
        password=SUBMIT_DATA_SETTINGS["password"],
        database=SUBMIT_DATA_SETTINGS["database"],
        charset="utf8"
    )
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM record_data"
    cursor.execute(sql)
    r = cursor.fetchone()
    count = r[0]
    skip_len = df.shape[0]
    if count > skip_len:
        df = df.iloc[:0]
        sql = "SELECT * FROM record_data"
        cursor.execute(sql)
        for i in tqdm(range(count)):
            if i < skip_len:
                continue
            r = cursor.fetchone()
            data = {
                "user": "",
                "datetime": r[2].strftime("%Y-%m-%d %H:%M:%S"),
                "oxycola": r[3],
                "coolant": r[4],
                "tempura": r[5],
                "repair": r[6],
                "ammo": r[7],
                "klxd1": r[8],
                "klxd2": r[9],
                "klxd3": r[10],
                "wsk1": r[11],
                "wsk2": r[12],
                "wsk3": r[13],
                "zwzg1": r[14],
                "zwzg2": r[15],
                "zwzg3": r[16],
                "blk1": r[17],
                "blk2": r[18],
                "blk3": r[19],
                "coin1": r[20],
                "coin2": r[21],
                "coin3": r[22],
                "coin4": r[23],
                "j113": r[24],
            }
            if r[1] == 1:
                data["user"] = "VirtualRiot"
            elif r[1] == 2:
                data["user"] = "凌影QAQ"
            df = df.append([data], ignore_index=True)
            df.to_csv(PATH["submit_data_file_path"], mode="a", encoding="GB2312", index=False, header=False)
            df = df.iloc[:0]
        print("Updating submit_data ...  Done")
    cursor.close()
    conn.close()


def main():
    print("Submitting commit_data...")
    update_local_submit_data()
    commit_data_file = pd.read_csv(PATH["commit_data_file_path"], encoding="GB2312")
    submit_data_file = pd.read_csv(PATH["submit_data_file_path"], encoding="GB2312")
    cdf = pd.DataFrame(commit_data_file)
    sdf = pd.DataFrame(submit_data_file).iloc[:0]
    verify_code = SUBMIT_DATA_SETTINGS["verify_code"]
    if cdf.shape[0] > 0:
        for i in tqdm(range(cdf.shape[0])):
            c = cdf.iloc[i: i + 1].drop(columns=["checked", "folder"])
            data_list = c.iloc[0].values.tolist()[2:]
            data_list = [str(s) for s in data_list]
            data_list[17:21] = [s.zfill(3) for s in data_list[17:21]]
            data_code = "".join([str(num) for num in data_list])
            sdf = sdf.append(c, ignore_index=True)
            submit_data(data_code, verify_code)
            sdf.to_csv(PATH["submit_data_file_path"], mode="a", encoding="GB2312", index=False, header=False)
            time.sleep(0.1)
            sdf = sdf.iloc[:0]
        move_image()
        cdf = cdf.iloc[:0]
        cdf.to_csv(PATH["commit_data_file_path"], encoding="GB2312", index=False)
        print("Success <submit passed>")
    else:
        print("Error <commit data not found>")


if __name__ == "__main__":
    main()
