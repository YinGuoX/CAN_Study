from asammdf import MDF

"""
将mf4格式 复制后 合并一份=>相同结构可以进行合并？
"""


f = r"./input/demo.mf4"
f1 = r"./input/demo_shou.mf4"
f2 = r"./input/demo_copy.mf4"
mdf = MDF(f)
mdf_copy = MDF(f1)
mdf_code_copy = MDF(f2)
print(mdf.info())
print(mdf_copy.info())
print(mdf_code_copy.info())
signal = mdf.get(group=0, index=0).copy()
# signal.plot()
print(signal)
# API内置的合并=>相同结构可以合并！
mdf_concat = MDF.concatenate([mdf,mdf_copy])
# TODO：mdf_copy的数据不一样，导致直接拼接会有问题！
mdf_concat = MDF.concatenate([mdf,mdf_code_copy])
print(mdf_concat.info())
signal = mdf_concat.get(group=0, index=0).copy()
print(signal)