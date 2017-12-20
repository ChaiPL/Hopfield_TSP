from numpy import random

def CreateCity(GetNum):
    cityNum = GetNum
    city = []
    for i in range(cityNum):
        temp = []
        for j in range(2):
           temp.append(random.randint(0, 350))
        city.append(temp)
    return city
