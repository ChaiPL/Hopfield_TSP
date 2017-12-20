import Hopfield_Ui
from Hopfield_CreateCity import CreateCity

# 城市坐标
# city_address = [(25, 120), (240, 55), (330, 50), (295, 275), (100, 35), (90, 290), (245, 110), (295, 165)]
city_address = CreateCity(8)
Hopfield_Ui.run(city_address)


