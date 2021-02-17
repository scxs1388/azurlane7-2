# map object indices list
object_index = [
    [(0, 0), "A1"], [(0, 2), "C1"], [(0, 4), "E1"], [(0, 5), "F1"],
    [(1, 6), "G2"],
    [(2, 0), "A3"], [(2, 2), "C3"], [(2, 4), "E3"], [(2, 6), "G3"],
    [(3, 1), "B4"], [(3, 5), "F4"],
    [(4, 2), "C5"], [(4, 3), "D5"], [(4, 5), "F5"],
    [(4, 4), "E5"],
    [(1, 0), "A2"], [(1, 3), "D2"], [(2, 7), "H3"], [(3, 3), "D4"]
]

# object adjacency list
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

# coordinates of click and recognition points
coordinates = {
    "A1": [717, 397],
    "A2": [712, 400],
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
    "TeamChange": [1250, 970],
    "AssignmentVerify": [970, 610],
    "VictoryPoint": [1350, 275],
    "VictoryConfirm": [1300, 740],
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
    "SR": "5A4D84",
    "SSR": "92703D"
}