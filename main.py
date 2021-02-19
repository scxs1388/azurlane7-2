import os
import sys

import pyautogui

import funcs


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
            level = funcs.AzurlaneLevel7_2(c)
            level.run()
            c += 1
    except funcs.SevereDamageException:
        level.defeat()
        main(count - c + 1)

    
if __name__ == "__main__":
    try:
        root_dir = os.path.join(sys.path[0], "image")
        if not os.path.isdir(root_dir):
            os.makedirs(root_dir)
        text = pyautogui.prompt(text='请输入需要通关的次数(必须是正整数)', title='输入', default='50')
        if text.isdigit():
            cnt = int(text)
            main(cnt)
        else:
            raise RuntimeError
    except RuntimeError:
        print("Invalid Input.")
