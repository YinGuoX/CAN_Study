from asammdf import MDF

"""
将mf4格式转换为asc,csv格式
"""

f = r"./input/demo.mf4"
mdf = MDF(f)
print(mdf.info())
empty_channels = "c"
# 通过mdf.virtual_groups获取到全部的channel group
# 获取该虚拟组中所有的通道
channels = []
for group_index, (virtual_group_index, virtual_group) in enumerate(mdf.virtual_groups.items()):
    if virtual_group.cycles_nr == 0 and empty_channels == "skip":
        continue
    # mdf.included_channels(virtual_group_index)方法获取到当前channel group下包含的channels
    # 获取的channels是一个元组列表，第一个都是None,第二个和第三个分别是channel group的index和channel的index，
    # mdf.get()方法的参数其实有很多，前三个是signal name，group index，channel index，其实就是列表元组的三个，因为channel group、channel是一个二维结构，所以，其实可以不用信号名来获取信号，也可以通过group index，和channel index，然后第一个参数传None，
    included_channels = mdf.included_channels(virtual_group_index)[virtual_group_index]
    for gp_index, channel_indexes in included_channels.items():
        for ch_index in channel_indexes:
            # 排除主通道
            # 在CAN总线中，每个节点都有一个唯一的标识符，称为节点ID。主通道是用于接收和发送节点ID的通道，因此它不应该被视为普通的数据通道。在这段代码中，排除主通道是为了避免将主通道误认为是普通的数据通道，从而导致数据处理错误。
            if ch_index != mdf.masters_db.get(gp_index, None):
                channels.append((None, gp_index, ch_index))
    print(channels)
# mdf.export("csv",filename="test.csv",channels=channels,raw=False)
# mdf.export("csv",filename="test1.csv")
print("convert to asc done")