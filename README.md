# azurlane7-2
A Python-based RPA script for Azur Lane level 7-2.

## 1 Requirements
### Hardware
1. OS: __Windows 10__
2. Screen Size: __1920x1080__
### Software
1. MuMu Android Simulator
    - Screen Resolution: __width: 1200__, __height: 1200__, __DPI: 320__, __maximized window__
2. Python Environment
    - Python Version: > 3.0.0
    - PyAutoGUI

## 2 Usage
1. Clone this repository to your specified directory:
```git
git clone https://github.com/scxs1388/azurlane7-2.git
```
2. Install Python3 or create Anaconda3 environment. (Recommended Python Version: 3.6.12)
### 2.1 Simple Usage (data recording excluded)
3. Install PyAutoGUI.
```
pip install pyautogui
```
4. Set the game interface on campaign Chapter 7.
5. Set the option `RECORD_ITEM` to `False` in the file `settings.py`.
6. Run the file `main.py` in cmd. (admin rights required)
```python
python main.py
```
7. Input 7-2 pass times and confirm.
8. Switch to the game interface.

### 2.2 Advanced Usage (data recording included)
9. Install following modules:
```
pip install numpy
pip install pandas
pip install opencv-python
pip install tqdm
pip install baidu-aip
pip install PyMySQL
```
10. Set the option `RECORD_ITEM` to `True` in the file `settings.py`
11. Record Data

    All screenshot images will be saved in the directory `image/commit_image`.

12. Commit Data
    - run the file `commit_data.py`. (__Baidu AI client info required__)
    - check the data file `data/commit_data.csv` and correct the recognition errors.
    - run the file `commit_data.py` again to check the data validity.

13. Submit Data
    - run the file `submit_data.py`. (__server user info required__)
    - the file `data/commit_data.csv` will be reset, the file `data/submit_data.csv` will be updated, the image file directories in `image/commit_image` will be moved to `image/submit_image`. 

## 3 Who's Afraid Of 7-2 ?
a website to display the statistics of the dropped items in level 7-2. url: `https://www.scxs-studio.com/p/7-2/`

## 4 About developers
Azurlane(CN) 水星行动 VirtualRiot
        
