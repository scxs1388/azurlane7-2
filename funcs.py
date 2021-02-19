import os
import shutil
import sys
import time

import pyautogui
import tqdm

from map_data import *


class SevereDamageException(BaseException):
    def __init__(self):
        super().__init__()


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
    pyautogui.leftClick(x, y)
    time.sleep(interval)


class AzurlaneLevel7_2():
    def __init__(self, number):
        self.v = [object_code["blank"] for i in range(15)] + [object_code["item"] for i in range(4)] + [object_code["blank"]]
        self.index = 0
        self.savedir = os.path.join(os.path.join(sys.path[0], "image"), str(len(os.listdir(os.path.join(sys.path[0], "image"))) + 1))
        self.number = number

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
        elif self.index == 5:
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

    def move(self, target):
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
            click(target_x, target_y, (distance + 0.9) / 2)

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
        if self.index == 6:
            self.save_image(5)
        click(coordinates["VictoryConfirm"][0], coordinates["VictoryConfirm"][1], 2)
        current_image = pyautogui.screenshot()
        if color_match(get_color(current_image, coordinates["SRPoint"][0], coordinates["SRPoint"][1]), function_colors["SR"]):
            click(coordinates["VictoryConfirm"][0], coordinates["VictoryConfirm"][1], 2)
        click(coordinates["VictoryConfirm"][0], coordinates["VictoryConfirm"][1], 2)
        click(coordinates["AssignmentVerify"][0], coordinates["AssignmentVerify"][1], 3)
    
    def defeat(self):
        """
        Restart After Defeat
        :return:
        """
        print(f"{self.number}\tDefeat")
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
        self.scan_map()
        if self.index == 1:
            enemy_list = [[i, [i, i]] for i, ei in enumerate(self.v[:14]) if object_code["l1"] <= ei <= object_code["t3"] and i > 0]
            target = self.find_top_priority_enemy(enemy_list)
            self.move(target)
            self.victory()
            self.v[target[0]] = object_code["team1"]
            self.v[-1] = -1
        if 2 <= self.index <= 4:
            enemy_list = self.find_reachable_target()
            target = self.find_top_priority_enemy(enemy_list)
            self.move(target)
            self.victory()
            self.v[self.v.index(object_code["team1"])] = object_code["scrap"]
            self.v[target[0]] = object_code["team1"]
        if self.index == 5:
            item_list = self.find_reachable_target()
            for i, item in enumerate(item_list):
                self.move(item)
                self.save_image(i)
                time.sleep(1)
                click(960, 810, 1)
            enemy_list = [[i, [i, i]] for i, ei in enumerate(self.v[:14]) if object_code["l1"] <= ei <= object_code["t3"]]
            target = self.find_top_priority_enemy(enemy_list)
            self.move(target)
            self.victory()
            self.v[self.v.index(object_code["team1"])] = object_code["scrap"]
            self.v[target[0]] = object_code["team1"]
        if self.index == 6:
            click(coordinates["SwitchOver"][0], coordinates["SwitchOver"][1], 1.25)
            click(coordinates[f"Boss{self.v[-1]}"][0], coordinates[f"Boss{self.v[-1]}"][1], 2)
            self.victory()

    def start(self):
        """
        Enter level 7-2
        :return:
        """
        time.sleep(1)
        click(coordinates["7-2Select"][0], coordinates["7-2Select"][1], 0.5)
        click(coordinates["ImmediateStart"][0], coordinates["ImmediateStart"][1], 0.5)
        click(coordinates["WeighAnchor"][0], coordinates["WeighAnchor"][1], 1)
        click(coordinates["AssignmentVerify"][0], coordinates["AssignmentVerify"][1], 3)

    def run(self):
        """
        Single Entire 7-2 Process
        :return:
        """
        os.mkdir(self.savedir)
        self.start()
        for i in range(1, 7):
            self.index = i
            self.battle()
        if len(os.listdir(self.savedir)) < 5:
            shutil.rmtree(self.savedir)
            print(f"{self.number}\tVictory (no item)")
        else:
            print(f"{self.number}\tVictory")
