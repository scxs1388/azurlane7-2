import os
import sys
from settings import PATH
from random import shuffle, randint
from tqdm import tqdm
# e = [
#     [15],  # 0
#     [16, 2],  # 1
#     [1, 16, 8, 4, 3, 7, 10],  # 2
#     [2, 4, 7, 8 ,10, 17, 16],  # 3
#     [2, 3, 7, 8, 10, 17, 16],  # 4
#     [6, 9, 11, 15],  # 5
#     [18, 5, 7, 9, 11, 16],  # 6
#     [2, 8, 3, 4, 10, 12, 13, 16, 18, 6],  # 7
#     [2, 3, 7, 10, 17, 16],  # 8, 4
#     [5, 6, 11, 18],  # 9
#     [7, 8, 12, 13, 2, 16, 18, 3, 4],  # 10
#     [5, 6, 9, 12, 18],  # 11
#     [11, 14, 13, 18],  # 12
#     [7, 12, 18],  # 13, 10
#     [7, 10],  # 14
#     [0, 5],  # 15
#     [1, 2, 6, 7, 8, 4, 3, 18],  # 16
#     [8, 4, 3],  # 17
#     [6, 7, 9, 10, 11, 12, 13, 16]  # 18
# ]
object_index = [
    [(0, 0), "A1"], [(0, 2), "C1"], [(0, 4), "E1"], [(0, 5), "F1"],
    [(1, 6), "G2"],
    [(2, 0), "A3"], [(2, 2), "C3"], [(2, 4), "E3"], [(2, 6), "G3"],
    [(3, 1), "B4"], [(3, 5), "F4"],
    [(4, 2), "C5"], [(4, 3), "D5"], [(4, 5), "F5"],
    [(4, 4), "E5"],
    [(1, 0), "A2"], [(1, 3), "D2"], [(2, 7), "H3"], [(3, 3), "D4"]
]
enemy_mapping = {
    1: 2,
    2: 4,
    3: 6,
    4: 3,
    5: 5,
    6: 7,
    7: 1,
    8: 8,
    9: 9
}
class az72():
    def __init__(self):
        self.v = [0 for i in range(15)] + [10 for i in range(4)] + [0]
        self.index = 0
        self.item_count = 0
        self.e = [
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

    def scan_map(self):
        def gen_enemy():
            num = randint(0, 99)
            # 50 45 5 5/30/15 5/30/10 2/2/1
            l = [1] * 5 + [2] * 30 + [3] * 15 + [4] * 5 + [5] * 30 + [6] * 10 + [7] * 2 + [8] * 2 + [9] * 1
            return l[num]
        enemy_position = [i for i in range(14) if self.v[i] == 0]
        shuffle(enemy_position)
        if self.index == 1:
            self.v[enemy_position[0]] = gen_enemy()
            self.v[enemy_position[1]] = gen_enemy()
            self.v[enemy_position[2]] = gen_enemy()
        if 2 <= self.index <= 3:
            self.v[enemy_position[0]] = gen_enemy()
            self.v[enemy_position[1]] = gen_enemy()
        if self.index == 4:
            self.v[enemy_position[0]] = gen_enemy()
    def find_reachable_target(self):
        if self.index <= 5:
            enemy_list = []
            flag = [False for i in range(len(self.v))]
            queue = [[self.v.index(12), [self.v.index(12)]]]
            flag[self.v.index(12)] = True
            while len(queue) > 0:
                length = len(queue)
                while length > 0:
                    temp = queue.pop(0)
                    for i in self.e[temp[0]]:
                        if not flag[i]:
                            flag[i] = True
                            if self.v[i] == 0 or self.v[i] == 11:
                                queue.append([i, temp[1] + [i]])
                            if 1 <= self.v[i] <= 9:
                                enemy_list.append([i, temp[1] + [i]])
                    length -= 1
            return enemy_list
        else:
            item_list = []
            addone_flag = True
            while addone_flag:
                addone_flag = False
                queue = []
                flag = [False for i in range(len(self.v))]
                if len(item_list) == 0:
                    queue.append([self.v.index(10), [self.v.index(10)]])
                    flag[self.v.index(10)] = True
                else:
                    queue.append([item_list[-1][0], [item_list[-1][0]]])
                    flag[item_list[-1][0]] = True
                while len(queue) > 0 and not addone_flag:
                    length = len(queue)
                    while length > 0 and not addone_flag:
                        temp = queue.pop(0)
                        for i in self.e[temp[0]]:
                            if not flag[i]:
                                flag[i] = True
                                if self.v[i] == 0 or self.v[i] == 11 or self.v[i] == 12:
                                    queue.append([i, temp[1] + [i]])
                                if self.v[i] == 10:
                                    item_list.append([i, temp[1] + [i]])
                                    addone_flag = True
                                    self.v[i] = 11
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
                clear = [11, 12]
                if self.v[3] in clear or self.v[4] in clear or self.v[8] in clear:
                    keypoint4_flag = True
        if len(keypoint123_enemy) > 0:
            return sorted(keypoint123_enemy, key=get_distance)[-1]
        if len(keypoint4_enemy) > 0 and not keypoint4_flag:
            return sorted(keypoint4_enemy, key=get_category)[-1]
        return sorted(enemy_list, key=get_category)[-1]

    def battle(self):
        if self.index == 1:
            self.scan_map()
            enemy_list = [[i, [i, i]] for i, ei in enumerate(self.v[:14]) if 1 <= ei <= 9 and i > 0]
            target = self.find_top_priority_enemy(enemy_list)
            # self.record_logger(enemy_list, None, target)
            self.v[target[0]] = 12
            self.v[-1] = -1
        if 2 <= self.index <= 5:
            self.scan_map()
            enemy_list = self.find_reachable_target()
            target = self.find_top_priority_enemy(enemy_list)
            # self.record_logger(enemy_list, None, target)
            self.v[self.v.index(12)] = 11
            self.v[target[0]] = 12
        # if self.index == 5:
        #     enemy_list = [[i, [i, i]] for i, ei in enumerate(self.v[:14]) if 1 <= ei <= 9]
        #     target = self.find_top_priority_enemy(enemy_list)
        #     # self.record_logger(enemy_list, item_list, target)
        #     self.v[self.v.index(12)] = 11
        #     self.v[target[0]] = 12
        if self.index == 6:
            self.e[6].remove(16)
            self.e[16].remove(6)
            self.e[6].remove(7)
            self.e[7].remove(6)
            self.e[16].remove(18)
            self.e[18].remove(16)
            item_list = self.find_reachable_target()
            if len(item_list) < 4:
                exit()
            
            # item_list = self.find_reachable_target()
            # self.record_logger(None, item_list, None)
            # if len(item_list) <= 4:
            #     exit()
            # if self.item_count < 4:
            #     item_list = self.find_reachable_target()
            #     for i, item in enumerate(item_list):
            #         self.move(item, 1.25)
            #         if RECORD_ITEM:
            #             self.save_image(self.item_count + i + 1)
            #         time.sleep(1.25)
            #         click(960, 810, 1.0)
            #         self.item_count += 1
    
    def run(self):        
        with open(os.path.join(PATH["root_dir"], "move.txt"), "w") as file:
            file.write("")
        for i in range(1, 7):
            self.index = i
            self.battle()

    def record_logger(self, enemy_list, item_list, target):
        pass
        # with open(os.path.join(PATH["root_dir"], "move.txt"), "a") as file:
        #     fel = []
        #     for enemy in self.v[:14]:
        #         if enemy == 0:
        #             fel.append("  ")
        #         elif 1 <= enemy <= 9:
        #             fel.append(f"e{enemy}")
        #         elif enemy == 11:
        #             fel.append("--")
        #         elif enemy == 12:
        #             fel.append("T1")
        #     file.writelines(f"==============={self.index}===============\n")
        #     file.writelines("┌─┬─┬─┬─┬─┬─┬─┬─┐\n")
        #     file.writelines(f"│{fel[0]}│□│{fel[1]}│  │{fel[2]}│{fel[3]}│  │  │\n")
        #     file.writelines("├─┼─┼─┼─┼─┼─┼─┼─┤\n")
        #     file.writelines(f"│？│□│□│？│  │  │{fel[4]}│  │\n")
        #     file.writelines("├─┼─┼─┼─┼─┼─┼─┼─┤\n")
        #     file.writelines(f"│{fel[5]}│  │{fel[6]}│BS│{fel[7]}│  │{fel[8]}│？│\n")
        #     file.writelines("├─┼─┼─┼─┼─┼─┼─┼─┤\n")
        #     file.writelines(f"│  │{fel[9]}│  │？│  │{fel[10]}│□│□│\n")
        #     file.writelines("├─┼─┼─┼─┼─┼─┼─┼─┤\n")
        #     file.writelines(f"│  │  │{fel[11]}│{fel[12]}│  │{fel[13]}│□│□│\n")
        #     file.writelines("└─┴─┴─┴─┴─┴─┴─┴─┘\n")
        #     file.writelines("\n")
        #     if enemy_list:
        #         file.writelines("enemy list:\n")
        #         for ei in enemy_list:
        #             file.writelines(f"{str(ei)}\n")
        #         file.writelines("\n")
        #     if item_list:
        #         file.writelines("item list:\n")
        #         for ei in item_list:
        #             file.writelines(f"{str(ei)}\n")
        #         file.writelines("\n")
        #     file.writelines("target:\n")
        #     file.writelines(f"{str(target)}\n\n")
                
    # ┌┬┐ ─
    # ├┼┤
    # └┴┘

if __name__ == "__main__":
    for i in tqdm(range(100000)):
        c = az72()
        c.run()