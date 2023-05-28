import asammdf

# 创建一个空的mdf文件
mdf = asammdf.MDF(version="4.10")

# 定义信号的conversion属性
conversion = {
    "slope": 0.1,
    "intercept": 0.0,
    "unit": "m/s",
    "type": "float32"
}

# 创建一个包含conversion属性的信号
signal = asammdf.Signal(
    name="Velocity",
    samples=[1.0, 2.0, 3.0],
    timestamps=[0.0, 1.0, 2.0],
    conversion=conversion
)

# 将信号添加到mdf文件中
mdf.append(signal)

# 保存mdf文件
mdf.save("example.mdf")

mdf1 = asammdf.MDF("example.mf4")
print(mdf1)
sig = mdf1.get("Velocity")
print(sig)