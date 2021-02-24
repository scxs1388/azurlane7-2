import os
import sys
import time

import pyautogui
from settings import RECORD_ITEM, PATH

# map object indices list
# [(matrix index x, matrix index y), game map indices "yx"]
object_index = [
    [(0, 0), "A1"], [(0, 2), "C1"], [(0, 4), "E1"], [(0, 5), "F1"],
    [(1, 6), "G2"],
    [(2, 0), "A3"], [(2, 2), "C3"], [(2, 4), "E3"], [(2, 6), "G3"],
    [(3, 1), "B4"], [(3, 5), "F4"],
    [(4, 2), "C5"], [(4, 3), "D5"], [(4, 5), "F5"],
    [(4, 4), "E5"],
    [(1, 0), "A2"], [(1, 3), "D2"], [(2, 7), "H3"], [(3, 3), "D4"]
]

# map object hashcode list
# l: light, m: main, t: treasure
object_code = {
    "blank": 0,
    "l1": 1,
    "l2": 2,
    "l3": 3,
    "m1": 4,
    "m2": 5,
    "m3": 6,
    "t1": 7,
    "t2": 8,
    "t3": 9,
    "item": 10,
    "scrap": 11,
    "team1": 12
}

# enemy priority ranking map
enemy_mapping = {
    object_code["l1"]: 2,
    object_code["l2"]: 4,
    object_code["l3"]: 6,
    object_code["m1"]: 3,
    object_code["m2"]: 5,
    object_code["m3"]: 7,
    object_code["t1"]: 1,
    object_code["t2"]: 8,
    object_code["t3"]: 9
}

# object adjacency list
e = [
    [15],  # 0
    [16, 2],  # 1
    [1, 16, 8, 4, 3, 7, 10],  # 2
    [2, 4, 7, 8 ,10, 17, 16],  # 3
    [2, 3, 7, 8, 10, 17, 16],  # 4
    [6, 9, 11, 15],  # 5
    [18, 5, 7, 9, 11, 16],  # 6
    [2, 8, 3, 4, 10, 12, 13, 16, 18, 6],  # 7
    [2, 3, 7, 10, 17, 16],  # 8, 4
    [5, 6, 11, 18],  # 9
    [7, 8, 12, 13, 2, 16, 18, 3, 4],  # 10
    [5, 6, 9, 12, 18],  # 11
    [11, 14, 13, 18],  # 12
    [7, 12, 18],  # 13, 10
    [7, 10],  # 14
    [0, 5],  # 15
    [1, 2, 6, 7, 8, 4, 3, 18],  # 16
    [8, 4, 3],  # 17
    [6, 7, 9, 10, 11, 12, 13, 16]  # 18
]

# coordinates of click and recognition points
coordinates = {
    "A1": [717, 397],
    "A2": [712, 444],
    "A3": [708, 492],
    "B4": [775, 542],
    "C1": [852, 397],
    "C3": [849, 492],
    "C5": [845, 594],
    "D2": [921, 444],
    "D4": [919, 542],
    "D5": [918, 594],
    "E1": [988, 397],
    "E3": [989, 492],
    "E5": [991, 594],
    "F1": [1056, 397],
    "F4": [1062, 542],
    "F5": [1064, 594],
    "G2": [1127, 444],
    "G3": [1130, 492],
    "H3": [1199, 492],
    "Start1": [710, 555],
    "Start2": [1203, 360],
    "Boss1": [1160, 420],
    "Boss2": [665, 620],
    "7-2Select": [850, 400],
    "ImmediateStart": [1200, 640],
    "WeighAnchor": [1275, 700],
    "Withdraw": [1100, 970],
    "SwitchOver": [1250, 970],
    "AssignmentVerify": [970, 610],
    "VictoryPoint": [1350, 275],
    "VictoryConfirm": [1300, 740],
    "DefeatConfirm": [950, 700],
    "Confirm": [1075, 630],
    "SRPoint": [1362, 142]
}

# coordinates offsets of click and recognition points
offsets = {
    "level1": [8, -8],
    "level2": [6, -10],
    "level3": [6, -8],
    "category": [30, 15],
    "move": [30, 25]
}

# RGB colors for level recognition
# map indices: [level1, level2, level3]
level_colors = {
    "A1": ["FFF09C", "FFEB9C", "FF8284"],
    "A3": ["FDF1A0", "FFEB9C", "FF8284"],
    "B4": ["FFFAB2", "FFEC9C", "FF8384"],
    "C1": ["F1E99F", "FFEB9B", "FC8384"],
    "C3": ["FFF3A5", "FFEB9C", "FF8284"],
    "C5": ["FFA3A5", "FFEB9C", "FF8284"],
    "D5": ["FFF3A5", "FFEB9C", "FF8284"],
    "E1": ["FFF7AC", "FFED9C", "FF8484"],
    "E3": ["F4ECA7", "FFEC9C", "FB8486"],
    "F1": ["FCF09D", "FFEB9C", "FF8284"],
    "F4": ["FFF3A7", "FFEB9C", "FF8284"],
    "F5": ["FEF0A0", "FFEB9C", "FF8284"],
    "G2": ["FFF6AC", "FFEB9C", "FE8284"],
    "G3": ["FFF9B0", "FFEC9C", "FE8384"],
}

# RGB colors for category recognition
# map indices: [light, main, treasure]
category_colors = {
    "A1": ["EFEBEF", "4C454C", "C4AF5A"],
    "A3": ["EFEBEF", "474547", "E3C57B"],
    "B4": ["EBE9EF", "3D3E3D", "C39756"],
    "C1": ["EDE9ED", "3F3A3F", "C4AC5B"],
    "C3": ["EFEBEF", "464446", "111111"],
    "C5": ["E9E7EF", "464646", "B6823B"],
    "D5": ["E4E3EA", "424142", "B68B47"],
    "E1": ["EFEBEF", "443F44", "C6AE5D"],
    "E3": ["EAE8EA", "3C3C3C", "CDA360"],
    "F1": ["EFEBEF", "453E45", "C4B05D"],
    "F4": ["EBE9EE", "484648", "D1AB66"],
    "F5": ["DCDDE2", "403D40", "C19852"],
    "G2": ["ECE8EC", "3A343A", "D1C071"],
    "G3": ["ECE8EC", "434343", "C9A65A"]
}

# RGB colors for functional recognition
function_colors = {
    "Team2": "FFFFFF",
    "VictoryPoint": "6382B5",
    "DefeatPoint": "A95152",
    "SR": "5A4D84",
    "SSR": "92703D"
}


class SevereDamageException(BaseException):
    def __init__(self):
        super().__init__()


def execute_time(func):
    def test(*args, **kwargs):
        start = time.time()
        f = func(*args, **kwargs)
        print(f"Time: {round(time.time() - start, 2)} s")
        return f
    return test


def get_color(image, x, y):
    """
    Get RGB Color From Screen By Coordinates
    :param image: Image Object
    :param x: coordinate X
    :param y: coordinate Y
    :return: str RGB color
    """
    r, g, b = image.getpixel((x, y))
    return (str(hex(r))[2:].zfill(2) + str(hex(g))[2:].zfill(2) + str(hex(b))[2:].zfill(2)).upper()


def color_match(c1: str, c2: str) -> bool:
    """
    Color Matching Function
    :param c1: str RGB color1
    :param c2: str RGB color2
    :return: bool (match: True, dismatch: False)
    """
    rgb1 = [int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)]
    rgb2 = [int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)]
    distance = (rgb1[0] - rgb2[0]) ** 2 + (rgb1[1] - rgb2[1]) ** 2 + (rgb1[2] - rgb2[2]) ** 2
    difference = (distance / 195075) ** 0.5  # 255^2*3
    if difference > 0.0125:  # 1.25%
        return False
    return True


def click(x, y, interval):
    """
    Click And Delay
    :param x: coordinate x
    :param y: coordinate y
    :param interval: Delay Time
    :return:
    """
    pyautogui.leftClick(x, y)
    time.sleep(interval)


class AzurlaneLevel7_2():
    def __init__(self, number):
        self.v = [object_code["blank"] for i in range(15)] + [object_code["item"] for i in range(4)] + [object_code["blank"]]
        self.index = 0
        self.savedir = ""
        if RECORD_ITEM:
            self.savedir = os.path.join(PATH["commit_image_dir"], str(len(os.listdir(PATH["commit_image_dir"])) + 1))
        self.number = number
        # self.item_count = 0

    def scan_map(self):
        """
        Get All Object Info On Current Map
        :param v: [vertex list]
        :return: [vertex list]
        """
        map_image = pyautogui.screenshot()
        for i, ei in enumerate(object_index[:14]):
            if self.v[i] == 0:
                category_flag, level_flag, category = False, False, 0
                level_color = [get_color(map_image, coordinates[ei[1]][0] + offsets[f"level{i}"][0], coordinates[ei[1]][1] + offsets[f"level{i}"][1]) for i in range(1, 4)]
                category_color = get_color(map_image, coordinates[ei[1]][0] + offsets["category"][0], coordinates[ei[1]][1] + offsets["category"][1])
                for j, c in enumerate(category_colors[ei[1]]):
                    if color_match(category_color, c):
                        category += j * 3
                        category_flag = True
                        break
                for j, c in enumerate(level_colors[ei[1]]):
                    if color_match(level_color[j], c):
                        category += j + 1
                        level_flag = True
                        break
                if category_flag and level_flag:
                    self.v[i] = category
        if self.index == 2:
            team2_position1_color = get_color(map_image, coordinates["Start1"][0], coordinates["Start1"][1])
            team2_position2_color = get_color(map_image, coordinates["Start2"][0], coordinates["Start2"][1])
            if color_match(team2_position1_color, function_colors["Team2"]):
                self.v[-1] = 1
            if color_match(team2_position2_color, function_colors["Team2"]):
                self.v[-1] = 2

    def find_reachable_target(self):
        """
        Find Reachable Target On Current Map
        :param v: [vertex list]
        :param index: battle index
        :return: [enemy object list]
        """
        if self.index <= 4:
            enemy_list = []
            flag = [False for i in range(len(self.v))]
            queue = [[self.v.index(object_code["team1"]), [self.v.index(object_code["team1"])]]]
            flag[self.v.index(object_code["team1"])] = True
            while len(queue) > 0:
                length = len(queue)
                while length > 0:
                    temp = queue.pop(0)
                    for i in e[temp[0]]:
                        if not flag[i]:
                            flag[i] = True
                            if self.v[i] == object_code["blank"] or self.v[i] == object_code["scrap"]:
                                queue.append([i, temp[1] + [i]])
                            if object_code["l1"] <= self.v[i] <= object_code["t3"]:
                                enemy_list.append([i, temp[1] + [i]])
                    length -= 1
            return enemy_list
        else:
            item_list = []
            for c in range(4):
                addone_flag = False
                queue = []
                flag = [False for i in range(len(self.v))]
                if c == 0:
                    queue.append([self.v.index(object_code["team1"]), [self.v.index(object_code["team1"])]])
                    flag[self.v.index(object_code["team1"])] = True
                else:
                    queue.append([item_list[-1][0], [item_list[-1][0]]])
                    flag[item_list[-1][0]] = True
                while len(queue) > 0 and not addone_flag:
                    length = len(queue)
                    while length > 0 and not addone_flag:
                        temp = queue.pop(0)
                        for i in e[temp[0]]:
                            if not flag[i]:
                                flag[i] = True
                                if self.v[i] == object_code["blank"] or self.v[i] == object_code["scrap"] or self.v[i] == object_code["team1"]:
                                    queue.append([i, temp[1] + [i]])
                                if self.v[i] == object_code["item"]:
                                    item_list.append([i, temp[1] + [i]])
                                    addone_flag = True
                                    self.v[i] = object_code["scrap"]
                            if addone_flag:
                                break
                        length -= 1
            return item_list 

    def find_top_priority_enemy(self, enemy_list):
        """
        Find The Top Priority Enemy In Current Enemy List
        :param v: [vertex list]
        :param enemy_list: [enemy object list]
        :return:
        """
        def get_category(ei):
            return enemy_mapping[self.v[ei[0]]]

        def get_distance(ei):
            x_distance = sum([abs(object_index[ei[1][i]][0][0] - object_index[ei[1][i - 1]][0][0]) for i in range(1, len(ei[1]))])
            y_distance = sum([abs(object_index[ei[1][i]][0][1] - object_index[ei[1][i - 1]][0][1]) for i in range(1, len(ei[1]))])
            return x_distance + y_distance
        keypoint123_enemy = []
        keypoint4_enemy = []
        keypoint4_flag = False
        for ei in enemy_list:
            if ei[0] == 5 or ei[0] == 6 or ei[0] == 7:
                keypoint123_enemy.append(ei)
            if ei[0] == 3 or ei[0] == 4 or ei[0] == 8:
                keypoint4_enemy.append(ei)
                clear = [object_code["team1"], object_code["scrap"]]
                if self.v[3] in clear or self.v[4] in clear or self.v[8] in clear:
                    keypoint4_flag = True
        if len(keypoint123_enemy) > 0:
            return sorted(keypoint123_enemy, key=get_distance)[-1]
        if len(keypoint4_enemy) > 0 and not keypoint4_flag:
            return sorted(keypoint4_enemy, key=get_category)[-1]
        return sorted(enemy_list, key=get_category)[-1]

    def save_image(self, num):
        """
        Save Screenshot Image (item & boss reward)
        :param: num: 1-4: item, 5: boss reward
        :return:
        """
        if num == 5:
            pyautogui.screenshot(os.path.join(self.savedir, "boss_reward.png"), region=(725, 410, 470, 215))
        else:
            pyautogui.screenshot(os.path.join(self.savedir, f"item_{num}.png"), region=(924, 470, 72, 98))
        time.sleep(0.5)

    def record_logger(self):
        if RECORD_ITEM:
            file = open(os.path.join(self.savedir, "log.txt"), "a")
            

    def move(self, target, delay):
        """
        Moving On Map
        :param: target: Map Object: [vertex_index, [path_point_list]]
        :return:
        """
        time.sleep(0.25)
        for i in range(1, len(target[1])):
            target_x = coordinates[object_index[target[1][i]][1]][0] + offsets["move"][0]
            target_y = coordinates[object_index[target[1][i]][1]][1] + offsets["move"][1]
            distance = abs(object_index[target[1][i]][0][0] - object_index[target[1][i - 1]][0][0]) + abs(object_index[target[1][i]][0][1] - object_index[target[1][i - 1]][0][1])
            click(target_x, target_y, (distance + 1.0) / 2 + delay)

    def victory(self):
        """
        Back To Map After Victory
        :param index: battle index
        :return:
        """
        time.sleep(5)
        victory_flag = False
        duration_time = 0
        interval = 2
        while not victory_flag:
            time.sleep(interval)
            duration_time += interval
            current_image = pyautogui.screenshot()
            victory_point_color = get_color(current_image, coordinates["VictoryPoint"][0], coordinates["VictoryPoint"][1])
            if color_match(victory_point_color, function_colors["VictoryPoint"]) or duration_time >= 180:
                victory_flag = True
            if color_match(victory_point_color, function_colors["DefeatPoint"]):
                raise SevereDamageException()
        click(coordinates["VictoryConfirm"][0], coordinates["VictoryConfirm"][1], 1.25)
        if self.index == 6 and RECORD_ITEM:
            self.save_image(5)
        click(coordinates["VictoryConfirm"][0], coordinates["VictoryConfirm"][1], 1.75)
        current_image = pyautogui.screenshot()
        if color_match(get_color(current_image, coordinates["SRPoint"][0], coordinates["SRPoint"][1]), function_colors["SR"]):
            click(coordinates["VictoryConfirm"][0], coordinates["VictoryConfirm"][1], 1.25)
        click(coordinates["VictoryConfirm"][0], coordinates["VictoryConfirm"][1], 2)
        click(coordinates["AssignmentVerify"][0], coordinates["AssignmentVerify"][1], 2.75)
    
    def defeat(self):
        """
        Restart After Defeat
        :return:
        """
        print(f"{self.number} -> \tDefeat")
        if RECORD_ITEM and os.path.exists(self.savedir):
            shutil.rmtree(self.savedir)
        time.sleep(0.5)
        click(coordinates["VictoryConfirm"][0], coordinates["VictoryConfirm"][1], 2.25)
        click(coordinates["VictoryConfirm"][0], coordinates["VictoryConfirm"][1], 2)
        click(coordinates["DefeatConfirm"][0], coordinates["DefeatConfirm"][1], 4.5)
        click(coordinates["AssignmentVerify"][0], coordinates["AssignmentVerify"][1], 2.5)
        click(coordinates["Withdraw"][0], coordinates["Withdraw"][1], 1)
        click(coordinates["Confirm"][0], coordinates["Confirm"][1], 5)
    
    def battle(self):
        """
        Middle & Boss Battle
        :param v: [vertex list]
        :param index: battle index (middle battle: 1-5, boss battle: 6)
        :return: v: [vertex list]
        """
        if self.index == 1:
            self.scan_map()
            enemy_list = [[i, [i, i]] for i, ei in enumerate(self.v[:14]) if object_code["l1"] <= ei <= object_code["t3"] and i > 0]
            target = self.find_top_priority_enemy(enemy_list)
            self.move(target, 0.25)
            self.victory()
            self.v[target[0]] = object_code["team1"]
            self.v[-1] = -1
        if 2 <= self.index <= 4:
            self.scan_map()
            enemy_list = self.find_reachable_target()
            target = self.find_top_priority_enemy(enemy_list)
            self.move(target, 0.25)
            self.victory()
            self.v[self.v.index(object_code["team1"])] = object_code["scrap"]
            self.v[target[0]] = object_code["team1"]
        if self.index == 5:
            if RECORD_ITEM:
                os.mkdir(self.savedir)
            item_list = self.find_reachable_target()
            for i, item in enumerate(item_list):
                self.move(item, 0.25)
                if RECORD_ITEM:
                    self.save_image(i + 1)
                time.sleep(1.25)
                click(960, 810, 1.0)
                # self.item_count += 1
            enemy_list = [[i, [i, i]] for i, ei in enumerate(self.v[:14]) if object_code["l1"] <= ei <= object_code["t3"]]
            target = self.find_top_priority_enemy(enemy_list)
            self.move(target, 0.25)
            self.victory()
            self.v[self.v.index(object_code["team1"])] = object_code["scrap"]
            self.v[target[0]] = object_code["team1"]
        if self.index == 6:
            # if self.item_count < 4:
            #     item_list = self.find_reachable_target()
            #     for i, item in enumerate(item_list):
            #         self.move(item, 1.25)
            #         if RECORD_ITEM:
            #             self.save_image(self.item_count + i + 1)
            #         time.sleep(1.25)
            #         click(960, 810, 1.0)
            #         self.item_count += 1
            click(coordinates["SwitchOver"][0], coordinates["SwitchOver"][1], 1.75)
            click(coordinates[f"Boss{self.v[-1]}"][0], coordinates[f"Boss{self.v[-1]}"][1], 2)
            self.victory()

    def start(self):
        """
        Enter level 7-2
        :return:
        """
        time.sleep(1)
        click(coordinates["7-2Select"][0], coordinates["7-2Select"][1], 0.75)
        click(coordinates["ImmediateStart"][0], coordinates["ImmediateStart"][1], 0.75)
        click(coordinates["WeighAnchor"][0], coordinates["WeighAnchor"][1], 1)
        click(coordinates["AssignmentVerify"][0], coordinates["AssignmentVerify"][1], 3)

    @execute_time
    def run(self):
        """
        Single Entire 7-2 Process
        :return:
        """
        self.start()
        for i in range(1, 7):
            self.index = i
            self.battle()
        if RECORD_ITEM:
            if len(os.listdir(self.savedir)) < 5:
                shutil.rmtree(self.savedir)
                print(f"{self.number}  -> \tVictory(no item)\t", end="")
            else:
                print(f"{self.number}  -> \tVictory\t\t", end="")
        else:
            print(f"{self.number}  -> \tVictory\t\t", end="")


def check_dir():
    if not os.path.isdir(PATH["data_dir"]):
        print("Initializing directory data ...    ", end="")
        os.makedirs(PATH["data_dir"])
        print("Done")
    if not os.path.exists(PATH["commit_data_file_path"]):
        print("Initializing file data/commit_data.csv ...  ", end="")
        df = pd.DataFrame(columns=[key for key in STANDARD_COMMIT_DATA_DICT])
        df.to_csv(PATH["commit_data_file_path"], encoding="GB2312", index=False)
        print("Done")
    if not os.path.exists(PATH["submit_data_file_path"]):
        print("Initializing file data/submit_data.csv ...  ", end="")
        df = pd.DataFrame(columns=[key for key in STANDARD_COMMIT_DATA_DICT]).drop(columns=["checked", "folder"])
        df.to_csv(PATH["submit_data_file_path"], encoding="GB2312", index=False)
        print("Done")
    update_local_submit_data()
    if not os.path.isdir(PATH["image_dir"]):
        print("Initializing directory image ...  ", end="")
        os.makedirs(PATH["image_dir"])
        print("Done")
    if not os.path.isdir(PATH["commit_image_dir"]):
        print("Initializing directory image/commit_image ...  ", end="")
        os.makedirs(PATH["commit_image_dir"])
        print("Done")
    if not os.path.isdir(PATH["submit_image_dir"]):
        print("Initializing directory image/submit_image ...  ", end="")
        os.makedirs(PATH["submit_image_dir"])
        print("Done")
    if not os.path.isdir(PATH["temp_image_dir"]):
        print("Initializing directory image/temp ...  ", end="")
        os.makedirs(PATH["temp_image_dir"])
        print("Done")
    if not os.path.isdir(PATH["sample_image_dir"]):
        print("Initializing directory image/sample_image ...  ", end="")
        shutil.move(os.path.join(PATH["root_dir"], "sample_image"), PATH["sample_image_dir"])
        print("Done")


def main(count):
    """
    Main Function
    :param count: 7-2 times
    :return:
    """
    c = 1
    try:
        level = None
        while c <= count:
            level = AzurlaneLevel7_2(c)
            level.run()
            c += 1
    except SevereDamageException:
        level.defeat()
        main(count - c)


if __name__ == "__main__":
    # python D:\Programming\Codefiles\pythonfiles\azurlane7-2\main.py
    try:
        if RECORD_ITEM:
            import shutil
            import pandas as pd
            import numpy as np
            from submit_data import update_local_submit_data
            from settings import STANDARD_COMMIT_DATA_DICT
            check_dir()
        text = pyautogui.prompt(text='请输入需要通关的次数(必须是正整数)', title='输入', default='50')
        if text.isdigit():
            cnt = int(text)
            print(f"Target: {cnt} Times")
            main(cnt)
        else:
            raise RuntimeError
    except RuntimeError:
        print("Invalid Input.")
