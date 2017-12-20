from math import sqrt
from typing import List, Tuple

def distance(p1, p2):
    return sqrt(pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2) )

def distance_matrix(coordinates : List[Tuple]):    #算出每两点之间的距离，并放入矩阵中表示
    matrix = []
    for cord1 in coordinates:
        row = []
        for cord2 in coordinates:
            row.append(distance(cord1, cord2))
        matrix.append(row)
    return matrix

def get_largest(matrix):
    largest = 0.0
    for x in range(0, len(matrix)):
        largest = largest if largest > max(matrix[x]) else max(matrix[x])
    return largest

def normalize(matrix):    #将距离矩阵中的值标准化至区间[0, 1]
    largest = get_largest(matrix)

    for x in range(0,len(matrix)):
        for y in range(0, len(matrix)):
            matrix[x][y] /= largest
    return matrix

def arrayTwoToOne(array2):        #将一个二维数组转化成两个一维数组
    x = []
    y = []
    num = len(array2)
    for i in range(num):
        x.append(array2[i][0])
        y.append(array2[i][1])
    return num, x, y

def arrayOneToTwo(arrayX, arrayY):       #将两个一维数组转化成一个二维数组
    array2 = []
    num = len(arrayX)
    for i in range(num):
        temp = []
        temp.append(arrayX[i])
        temp.append(arrayY[i])
        array2.append(temp)
    return array2

def distanceTwoPoints(x0, y0, x1, y1):
    return sqrt(pow((x1 - x0), 2) + pow((y1 - y0), 2))

def distanceLines(n, x, y):
    temp_distance = 0.0
    for i in range(n):
        start = i - 1
        end = i
        temp_distance += distanceTwoPoints(x[start], y[start], x[end], y[end])
    return temp_distance



