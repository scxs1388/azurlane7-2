import base64
import os
import sys
import time
from datetime import datetime

import cv2 as cv
import numpy as np
import pandas as pd
import requests
from tqdm import tqdm
from settings import PATH, COMMIT_DATA_SETTINGS, STANDARD_COMMIT_DATA_DICT

sample_items = [
    ("oxycola", os.path.join(PATH["temp_image_dir"], "oxycola.png")),
    ("coolant", os.path.join(PATH["temp_image_dir"], "coolant.png")),
    ("tempura", os.path.join(PATH["temp_image_dir"], "tempura.png")),
    ("repair", os.path.join(PATH["temp_image_dir"], "repair.png")),
    ("kit_t1", os.path.join(PATH["temp_image_dir"], "kit_t1.png")),
    ("kit_t2", os.path.join(PATH["temp_image_dir"], "kit_t2.png")),
    ("kit_t3", os.path.join(PATH["temp_image_dir"], "kit_t3.png")),
    ("coin", os.path.join(PATH["temp_image_dir"], "coin.png")),
    ("j113", os.path.join(PATH["temp_image_dir"], "j113.png"))
]


def ocr_scan(filepath, is_accurate):
    f = open(filepath, "rb")
    img = base64.b64encode(f.read())
    if len(COMMIT_DATA_SETTINGS["client_id"]) == 0:
        file = open(COMMIT_DATA_SETTINGS["client_info_file_path"])
        COMMIT_DATA_SETTINGS["client_id"] = file.readline()[:-1]
        COMMIT_DATA_SETTINGS["client_secret"] = file.readline()[:-1]
    url = f"https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={COMMIT_DATA_SETTINGS['client_id']}&client_secret={COMMIT_DATA_SETTINGS['client_secret']}"
    response = requests.get(url)
    if response:
        access_token = (response.json()["access_token"])
    if is_accurate:
        host = f"https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token={access_token}"
    else:
        host = f"https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={access_token}"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "image": img
    }
    res = requests.post(url=host, data=data, headers=headers)
    word_list = res.json()["words_result"]
    return word_list


def item_check(path, is_boss):
    src_img = cv.imread(path)
    res = []
    is_check = False
    threshold = 0.65
    sample_item_list = sample_items[:-1]
    if is_boss:
        res = ["j113", 0, True]
        threshold = 0.85
        sample_item_list = sample_items[-1:]
    for item in sample_item_list:
        tpl_img = cv.imread(item[1])
        r = cv.matchTemplate(src_img, tpl_img, cv.TM_CCOEFF_NORMED)
        loc = np.where(r > threshold)
        if len(loc[0]) > 0:
            if item[0] == "j113":
                max_loc = cv.minMaxLoc(r)[3]
                num_img = src_img[max_loc[1] + 46: max_loc[1] + 72, max_loc[0] + 50: max_loc[0] + 72]
                num_img_path = os.path.join(PATH["temp_image_dir"], item[0] + ".png")
                cv.imwrite(num_img_path, num_img)
                time.sleep(0.5)
                ocr_res = ocr_scan(num_img_path, True)
                if len(ocr_res) > 0:
                    num = ocr_res[0]["words"]
                    if num.isdigit():
                        res = [item[0], int(num), True]
                    else:
                        res = [item[0], -1, False]
                else:
                    res = [item[0], 0, True]
            elif item[0] == "coin":
                max_loc = cv.minMaxLoc(r)[3]
                num_img = src_img[max_loc[1] + 30: max_loc[1] + 75, max_loc[0] + 30: max_loc[0] + 72]
                num_img_path = os.path.join(PATH["temp_image_dir"], item[0] + ".png")
                cv.imwrite(num_img_path, num_img)
                time.sleep(1.0)
                ocr_res = ocr_scan(num_img_path, True)
                res = [item[0], -99999, False]
                if len(ocr_res) > 0:
                    num = ocr_res[0]["words"]
                    if num.isdigit():
                        if int(num) >= 100:
                            res = [item[0], int(num), True]
                        elif int(num) >= 90:
                            res = [item[0], int(num), False]
            elif "kit_t" in item[0]:
                max_loc = cv.minMaxLoc(r)[3]
                num_img = src_img[max_loc[1] + 72: max_loc[1] + 97, max_loc[0] + 1: max_loc[0] + 71]
                num_img_path = os.path.join(PATH["temp_image_dir"], item[0] + ".png")
                cv.imwrite(num_img_path, num_img)
                time.sleep(0.5)
                ocr_res = ocr_scan(num_img_path, False)
                res = ["blk3", -99999, False]
                if len(ocr_res) > 0:
                    category = ocr_res[0]["words"]
                    if "洛希" in category:
                        res = ["klxd" + item[0][5:], 1, True]
                    if "斯" in category:
                        res = ["wsk" + item[0][5:], 1, True]
                    if "王重" in category:
                        res = ["zwzg" + item[0][5:], 1, True]
                    if "鲁" in category:
                        res = ["blk" + item[0][5:], 1, True]
            else:
                res = [item[0], 1, True]
            is_check = True
            break
    if not is_check and not is_boss:
        res = ["ammo", 1, True]
    return res


def get_commit_data_dict(image_file_dir):
    item_data = []
    coin_data = [0, 0, 0, 0]
    commit_data_dict = STANDARD_COMMIT_DATA_DICT
    commit_data_dict["user"] = COMMIT_DATA_SETTINGS["USER"]
    commit_data_dict["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for i, f in enumerate(os.listdir(image_file_dir)):
        image_file_path = os.path.join(image_file_dir, f)
        if "item" in f:
            item_data.append(item_check(image_file_path, False))
        if "boss_reward" in f:
            item_data.append(item_check(image_file_path, True))
    if len(item_data) == 5:
        for i, item in enumerate(item_data):
            commit_data_dict["checked"] &= item[2]
            if item[0] == "coin":
                coin_data[coin_data.index(0)] = item[1]
            else:
                commit_data_dict[item[0]] += item[1]
        coin_data.sort(reverse=True)
        for i, coin in enumerate(coin_data):
            commit_data_dict[f"coin{i + 1}"] = coin
        return commit_data_dict
    else:
        return None
        

def check_validity():
    commit_data_file = pd.read_csv(PATH["commit_data_file_path"])
    df = pd.DataFrame(commit_data_file)
    flag = True
    index = 1
    for i in range(df.shape[0]):
        data_list = df.iloc[i].values.tolist()
        count = sum([num for num in data_list[2:19] if num > 0]) + len([num for num in data_list[19:23] if 90 <= num <= 225])
        if count != 4:
            print(f"{index} ->\t{df.loc[i, 'folder']}")
            flag = False
            index += 1
        elif data_list[-3] > 2 or data_list[-3] < 0:
            print(f"{index} ->\t{df.loc[i, 'folder']}")
            flag = False
            index += 1
    return flag


def main():
    print("Loading commit_data...")
    commit_data_file = pd.read_csv(PATH["commit_data_file_path"])
    df = pd.DataFrame(commit_data_file)
    skip_len = 0
    if df.shape[0] > 0:
        skip_len = df.shape[0]
        df = df.iloc[:0]
        # df.to_csv(PATH["commit_data_file_path"], encoding="GB2312", index=False)
    commit_image_dir_list = os.listdir(PATH["commit_image_dir"])
    if len(commit_image_dir_list) == 0:
        print("Error <commit image not found>")
    elif skip_len < len(commit_image_dir_list):
        for i in tqdm(range(len(commit_image_dir_list))):
            d = commit_image_dir_list[i]
            if i < skip_len:
                continue
            image_file_dir = os.path.join(PATH["commit_image_dir"], d)
            commit_data_dict = get_commit_data_dict(image_file_dir)
            if commit_data_dict:
                commit_data_dict["folder"] = d
                df = df.append([commit_data_dict], ignore_index=True)
                df.to_csv(PATH["commit_data_file_path"], mode="a", encoding="GB2312", index=False, header=False)
                df = df.iloc[:0]
    elif skip_len == len(commit_image_dir_list):
        is_valid = check_validity()
        if is_valid:
            print("Success <commit passed>")
        else:
            print("Complete <invalid data found>")
    else:
        print("Complete <extraction>")


if __name__ == "__main__":
    main()    
