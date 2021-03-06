#coding: utf-8

"""
Путь до бинарника rect.
"""
rect_path = '~/programming/rect/build/rect'


"""
Рабочая папка, там будут созданы все файлы и там будет происходить расчет.
"""
work_dir = "./test/"

"""
Параметры источника, задается в виде импульса Риккера, частота в Гц, координаты в м.
"""
source_frequency = 35.0
source_coords = [8500, 50.0]

"""
Приемники в виде файла. Файл вида:
x1 z1
x2 z2
...
и т.д.

for i in `seq 5 5 16900`; do echo $i 20; done > rec.txt
"""
receivers_coords = "rec.txt"

"""
Как часто сохранять в segy, время в секундах.
"""
dt = 0.0015

"""
Как часто сохранять vtk.
"""
dt_vtk = 0.01


"""
До какого момента времени считат, в секундах.
"""
t_max = 2


"""
Пути до файлов с параметрами модели.
"""
segy_p_wave = "MODEL_P-WAVE_VELOCITY_1.25m.segy"
segy_s_wave = "MODEL_S-WAVE_VELOCITY_1.25m.segy"
segy_rho    = "MODEL_DENSITY_1.25m.segy"

"""
Если модель не в единицах СИ, то надо ее переконвертировать.
Корректирующий параметр для координат модели и для значений.
"""
segy_scale_value  = 1.0
segy_scale_coords = 0.001



"""
Параметр, определяющий размер ячейки. Чем больше, тем меньше ячейка, соответственно больше узлов и дольше расчет.
Нормальные значения 5-15.
"""
cells_per_wave = 8
