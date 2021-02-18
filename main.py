import funcs
import pyautogui
import sys
import os


def main(count):
    """
    Main Function
    :param count: 7-2 times
    :return:
    """
    c = count
    try:
        while c > 0:
            funcs.run()
            c -= 1
    except funcs.SevereDamageException:
        funcs.defeat()
        main(count)

    
if __name__ == "__main__":
    try:
        dir_name = sys.path[0] + "\\image"
        if not os.path.isdir(dir_name):
            os.makedirs(dir_name)
        text = pyautogui.prompt(text='请输入需要通关的次数(必须是正整数)', title='输入', default='50')
        if text.isdigit():
            cnt = int(text)
            main(cnt)
        else:
            raise RuntimeError
    except RuntimeError:
        print("Invalid Input.")
