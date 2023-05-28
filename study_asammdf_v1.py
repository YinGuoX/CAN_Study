from asammdf import MDF

"""
 使用 asammdf 实现读取 mf4文件，单通道，单Channel，

"""

# dbc_path = r"./input/DX_CAN.dbc"
mdf_path= r"input/Acceleration_StandingStart.mf4"

mdf = MDF(mdf_path)
print(mdf)
print(mdf.info())

mdf_db = mdf.channels_db
print(mdf_db)

signal_list = list(mdf_db)
print(signal_list)

speed = mdf.get('VehicleSpeed')
speed.plot()

signals_data_frame = mdf.to_dataframe()
print(signals_data_frame)


