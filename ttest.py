import os
import sys
from settings import *

def record_logger():
    file = open(os.path.join(PATH["root_dir"], "move.txt"), "a")
    file.writelines("┌─┬─┬─┬─┬─┬─┬─┬─┐")
    file.writelines("│A│B│C│D│E│F│G│H│")



# ┌┬┐ ─
# ├┼┤
# └┴┘

if __name__ == "__main__":
    file = open(os.path.join(PATH["root_dir"], "move.txt"), "a")
    file.writelines(str([1, 2, 3]))
    file.close()