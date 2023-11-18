import time
import cv2
from matplotlib import pyplot as plt

pic_name = str(input("输入图片路径(不要带引号!):"))
size = str(input("输入导出图片的长宽(空格隔开,建议10 8):"))
strength = int(input("输入提取强度(越小特征越明显，0~255):"))
print('\n', '请等待...', '\n')
lenth = int(size.split(' ')[0])
high = int(size.split(' ')[-1])
feature_value = strength

# *********转换为灰度图*********#
img_16_list = []
img = cv2.imread(pic_name, cv2.IMREAD_GRAYSCALE)
img0 = img
img_list = []
flash_list = []
for it in img:
    for itt in it:
        flash_list.append(itt)
    img_list.append(flash_list)
    flash_list = []
# plt.savefig("灰度图.png")

line = len(img)
col = len(img[0])

# *********垂直边缘特征提取*********#
img_rol = []
for it in img_list:
    j = 0
    flash = it
    while True:
        sum1 = 0
        sum2 = 0
        try:
            for i in range(j, j + 3):
                sum1 += it[i]
            for i in range(j + 3, j + 6):
                sum2 += it[i]
            if abs(sum1 / 3 - sum2 / 3) > feature_value:
                flash[j] = 0
                flash[j + 1] = 0
            j += 3
        except IndexError:
            img_rol.append(flash)
            break
# plt.savefig("shu_zhi_te_zheng.png")


# *********垂直边缘特征筛选*********#
for j in range(0, col, 4):
    rol_4_list = []
    try:
        for i in range(0, line):
            rol_4_list.append(img_rol[i][j])
            rol_4_list.append(img_rol[i][j + 1])
            rol_4_list.append(img_rol[i][j + 2])
            rol_4_list.append(img_rol[i][j + 3])
        if rol_4_list.count(0) < 100:
            for i in range(0, line):
                img_rol[i][j] = img0[i][j]
                img_rol[i][j + 1] = img0[i][j + 1]
                img_rol[i][j + 2] = img0[i][j + 2]
                img_rol[i][j + 3] = img0[i][j + 3]
    except IndexError:
        pass

# *********水平边缘特征提取*********#
img_line = img_list
for i in range(col):
    for j in range(0, line, 3):
        sum1 = 0
        sum2 = 0
        try:
            for it in range(j, j + 3):
                sum1 += img_list[it][i]
            for it in range(j + 3, j + 6):
                sum2 += img_list[it][i]
            if abs(sum1 / 3 - sum2 / 3) > feature_value:
                img_line[j][i] = 0
                img_line[j + 1][i] = 0
        except IndexError:
            pass

# *********水平竖直特征重叠绘图*********#
pic_list = []
for i in range(line):
    flash = []
    for j in range(col):
        flash.append(0)
    pic_list.append(flash)

for i in range(line):
    for j in range(col):
        if img_rol[i][j] != 0:
            pic_list[i][j] = 255
        else:
            pass
        if img_line[i][j] != 0:
            pic_list[i][j] = 255
        else:
            pass

# 保存图片
plt.figure(figsize=(lenth, high))  # 6，8分别对应宽和高
plt.imshow(pic_list, cmap='gray', interpolation='nearest', vmin=0, vmax=255)
plt.savefig("D:/save.png", dpi=600)
plt.show()
time.sleep(3)
