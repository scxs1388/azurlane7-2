import ctypes
import logging
import os
import sys
import time
import pyautogui


object_index = [
    [(0, 0), "A1"], [(0, 2), "C1"], [(0, 4), "E1"], [(0, 5), "F1"],
    [(1, 6), "G2"],
    [(2, 0), "A3"], [(2, 2), "C3"], [(2, 4), "E3"], [(2, 6), "G3"],
    [(3, 1), "B4"], [(3, 5), "F4"],
    [(4, 2), "C5"], [(4, 3), "D5"], [(4, 5), "F5"],
    [(4, 4), "E5"],
    [(1, 0), "A2"], [(1, 3), "D2"], [(2, 7), "H3"], [(3, 3), "D4"]
]

e = [
    [15],
    [2, 16],
    [1, 3, 4, 7, 8, 10, 16],
    [2, 4, 7, 8 ,10, 16, 17],
    [2, 3, 7, 8, 10, 16, 17],
    [6, 9, 11, 15],
    [5, 7, 9, 11, 16, 18],
    [2, 3, 4, 6, 8, 10, 12, 13, 16, 18],
    [2, 3, 7, 10, 16, 17],  # 4
    [5, 6, 11, 18],
    [2, 3, 4, 7, 8, 12, 13, 16, 18],
    [5, 6, 9, 12, 18],
    [11, 13, 14, 18],
    [7, 12, 18],  # 10
    [7, 10],
    [0, 5],
    [1, 2, 3, 4, 6, 7, 8, 18],
    [3, 4, 8],
    [6, 7, 9, 10, 11, 12, 13, 16]
]

coordinates = {
    "A1": [717, 397],
    "A3": [708, 492],
    "B4": [775, 542],
    "C1": [852, 397],
    "C3": [849, 492],
    "C5": [845, 594],
    "D5": [918, 594],
    "E1": [988, 397],
    "E3": [989, 492],
    "E5": [991, 594],
    "F1": [1056, 397],
    "F4": [1062, 542],
    "F5": [1064, 594],
    "G2": [1127, 444],
    "G3": [1130, 492],
    "Start1": [710, 555],
    "Start2": [1203, 360],
    "Boss1": [1160, 420],
    "Boss2": [665, 620],
    "7-2Select": [850, 400],
    "ImmediateStart": [1200, 640],
    "WeighAnchor": [1275, 700],
    "TeamChange": [1250, 970],
    "AssignmentVerify": [970, 610],
    "VictoryPoint": [1350, 275],
    "VictoryConfirm": [1300, 740],
    "SRPoint": [1362, 142]
}

offsets = {
    "level1": [8, -8],
    "level2": [6, -10],
    "level3": [6, -8],
    "category": [30, 15],
    "move": [30, 25]
}

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

function_colors = {
    "Team2": "FFFFFF",
    "VictoryPoint": "6382B5",
    "SR": "5A4D84",
    "SSR": "92703D"
}


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def get_color(image, x, y):
    r, g, b = image.getpixel((x, y))
    return (str(hex(r))[2:].zfill(2) + str(hex(g))[2:].zfill(2) + str(hex(b))[2:].zfill(2)).upper()


def color_match(c1: str, c2: str) -> bool:
    rgb1 = [int(c1[0:2], 16), int(c1[2:4], 16), int(c1[4:6], 16)]
    rgb2 = [int(c2[0:2], 16), int(c2[2:4], 16), int(c2[4:6], 16)]
    distance = (rgb1[0] - rgb2[0]) ** 2 + (rgb1[1] - rgb2[1]) ** 2 + (rgb1[2] - rgb2[2]) ** 2
    difference = (distance / 195075) ** 0.5  # 255^2*3
    if difference > 1e-3:
        return False
    return True


def find_reachable_target(v, index):
    flag = [False for i in range(len(v))]
    queue = [[v.index(12), [v.index(12)]]]
    flag[v.index(12)] = True
    enemy_list = []
    item_list = []
    while len(queue) > 0:
        length = len(queue)
        while length > 0:
            temp = queue.pop(0)
            for i in e[temp[0]]:
                if not flag[i]:
                    flag[i] = True
                    if v[i] == 0 or v[i] == 11:
                        queue.append([i, temp[1] + [i]])
                    if 1 <= v[i] <= 9:
                        enemy_list.append([i, temp[1] + [i]])
                    if v[i] == 10:
                        item_list.append([i, temp[1] + [i]])
            length -= 1
    if index == 5:
        return item_list
    return enemy_list


def find_top_priority_enemy(v, enemy_list):
    enemy_mapping = {1: 7, 2: 1, 3: 4, 4: 2, 5: 5, 6: 3, 7: 6, 8: 8, 9: 9}
    def get_category(ei):
        return enemy_mapping[v[ei[0]]]
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
            if v[ei[0]] == 11:
                keypoint4_flag = True
    if len(keypoint123_enemy) > 0:
        return sorted(keypoint123_enemy, key=get_distance)[-1]
    if len(keypoint4_enemy) > 0 and not keypoint4_flag:
        return sorted(keypoint4_enemy, key=get_category)[-1]
    return sorted(enemy_list, key=get_category)[-1]


def scan_map(v):
    map_image = pyautogui.screenshot()
    # map_image = Image.open("C:/Users/10950/OneDrive/Pictures/untitled.png")
    for i, ei in enumerate(object_index[:14]):
        if v[i] == 0:
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
                v[i] = category
    if v[-1] == -1:
        team2_position1_color = get_color(map_image, coordinates["Start1"][0], coordinates["Start1"][1])
        team2_position2_color = get_color(map_image, coordinates["Start2"][0], coordinates["Start2"][1])
        if color_match(team2_position1_color, function_colors["Team2"]):
            v[-1] = 1
        if color_match(team2_position2_color, function_colors["Team2"]):
            v[-1] = 2
    return v


def move(target):
    for i in range(1, len(target[1])):
        target_x = coordinates[object_index[target[1][i]][1]][0] + offsets["move"][0]
        target_y = coordinates[object_index[target[1][i]][1]][1] + offsets["move"][1]
        distance = abs(object_index[target[1][i]][0][0] - object_index[target[1][i - 1]][0][1]) + abs(object_index[target[1][i]][0][1] - object_index[target[1][i - 1]][0][1])
        pyautogui.leftClick(target_x, target_y)
        time.sleep((distance + 1) / 2)


def victory():
    time.sleep(5)
    victory_flag = False
    duration_time = 0
    while not victory_flag:
        time.sleep(2)
        duration_time += 2
        current_image = pyautogui.screenshot()
        victory_point_color = get_color(current_image, coordinates["VictoryPoint"][0], coordinates["VictoryPoint"][1])
        if color_match(victory_point_color, function_colors["VictoryPoint"]) or duration_time >= 180:
            victory_flag = True
    pyautogui.leftClick(coordinates["VictoryConfirm"][0], coordinates["VictoryConfirm"][1])
    time.sleep(1.25)
    pyautogui.leftClick(coordinates["VictoryConfirm"][0], coordinates["VictoryConfirm"][1])
    time.sleep(2.25)
    current_image = pyautogui.screenshot()
    if color_match(get_color(current_image, coordinates["SRPoint"][0], coordinates["SRPoint"][1]), function_colors["SR"]):
        pyautogui.leftClick(coordinates["VictoryConfirm"][0], coordinates["VictoryConfirm"][1])
        time.sleep(2.25)
    elif color_match(get_color(current_image, coordinates["SRPoint"][0], coordinates["SRPoint"][1]), function_colors["SSR"]):
        pyautogui.leftClick(coordinates["VictoryConfirm"][0], coordinates["VictoryConfirm"][1])
        time.sleep(2.25)
    pyautogui.leftClick(coordinates["VictoryConfirm"][0], coordinates["VictoryConfirm"][1])
    time.sleep(2.25)
    pyautogui.leftClick(coordinates["AssignmentVerify"][0], coordinates["AssignmentVerify"][1])
    time.sleep(3)
    

def battle(v, index):
    v = scan_map(v)
    print(v)
    if index == 1:
        enemy_list = [[i, [i, i]] for i, ei in enumerate(v[1:14]) if 1 <= ei <= 9]
        target = find_top_priority_enemy(v, enemy_list)
        move(target)
        victory()
        v[target[0]] = 12
        v[-1] = -1
    if 2 <= index <= 4:
        enemy_list = find_reachable_target(v, index)
        target = find_top_priority_enemy(v, enemy_list)
        move(target)
        victory()
        v[v.index(12)] = 11
        v[target[0]] = 12
    if index == 5:
        item_list = find_reachable_target(v, index)
        for item in item_list:
            move(item)
        enemy_list = [[i, [i, i]] for i, ei in enumerate(v[:14]) if 1 <= ei <= 9]
        target = find_top_priority_enemy(v, enemy_list)
        move(target)
        victory()
        v[v.index(12)] = 11
        v[target[0]] = 12
    if index == 6:
        pyautogui.leftClick(coordinates[f"Boss{v[-1]}"][0], coordinates[f"Boss{v[-1]}"][1])
        victory()
    return v


def start():
    time.sleep(0.5)
    pyautogui.leftClick(coordinates["7-2Select"][0], coordinates["7-2Select"][1])
    time.sleep(0.5)
    pyautogui.leftClick(coordinates["ImmediateStart"][0], coordinates["ImmediateStart"][1])
    time.sleep(0.5)
    pyautogui.leftClick(coordinates["WeighAnchor"][0], coordinates["WeighAnchor"][1])
    time.sleep(1)
    pyautogui.leftClick(coordinates["AssignmentVerify"][0], coordinates["AssignmentVerify"][1])
    time.sleep(3)


def end():
    time.sleep(2)


def run():
    # v = [1, 2, 3, 4, 9, 12, 0, 0, 5, 6, 7, 8, 9, 9, 0, 10, 10, 10, 10]
    # blank = 0
    # enemy(zc1-zc3) = 1-3
    # enemy(zl1-ys3) = 4-6
    # enemy(ys1-ys3) = 7-9
    # items = 10
    # scrap = 11
    # team1 = 12
    # obstacle = 99
    time.sleep(5)
    start()
    v = [0 for i in range(14)] + [10 for i in range(4)] + [0]
    v = battle(v, 1)
    v = battle(v, 2)
    v = battle(v, 3)
    v = battle(v, 4)
    v = battle(v, 5)
    v = battle(v, 6)
    end()


if __name__ == "__main__":
    if is_admin():
        run()
    else:
        if sys.version_info[0] == 3:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            run()
        # else:  # in python2.x
        #     ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), unicode(__file__), None, 1)
