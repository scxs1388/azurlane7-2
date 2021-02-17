import funcs
import pyautogui


if __name__ == "__main__":
    try:
        text = pyautogui.prompt(text='请输入需要通关的次数(必须是正整数)', title='输入', default='50')
        if text.isdigit():
            count = int(text)
            while count > 0:
                funcs.run()
        else:
            raise RuntimeError
    except RuntimeError:
        print("Invalid Input.")
