from asammdf import MDF

"""
读取多通道的信号
"""

f = r"./input/demo.mf4"
mdf = MDF(f)

# 查看mf4文件的基本信息
mdf_info= mdf.info()
for k,v in mdf_info.items():
    print("=====")
    print(f"key={k}")
    print(f"value={v}")

# 获取所有信号名及其索引
chn_db = mdf.channels_db
print(chn_db)

"""
mdf文件一般是用channel和channel group组织的，
一个文件可能包含多个chnannel group，
一个channel group也可以包含多个channel，
channel和signal一一对应，
channel保存了一些描述信息，数据和时间戳保存在signal里
"""
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

# 可以用mdf.select方法筛选出我们需要的信号，信号和通道是一一对应关系，我们可以把这两个东西当成一个东西理解，只不过两种数据结构存的数据不一样
"""
mdf.select返回的是信号列表，而不是包含这些信号的mdf实列，
mdf.filter()返回的是mdf实列，这里需要注意下，还有那个raw参数，
虽然它这里用的True，但是，一般我们要设置为False，特别是自己处理数据的时候，因为设置成True会导致读出的数据错误，它之所以有这个参数，我怀疑是为了兼容一些数据格式，而不是为了数据准确性。
"""
for signal in mdf.select(channels, raw=True, copy_master=False, validate=False):
    print("11111111111111111")
    print(signal)
for sig_id in channels:
    if sig_id[2]==8:
        print(sig_id)
        signal = mdf.get(group=sig_id[1],index=sig_id[2])
        print(signal)