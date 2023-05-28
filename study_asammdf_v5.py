import copy

from asammdf import MDF
import asammdf

"""
将mf4格式 复制一份
"""

f = r"./input/demo.mf4"
mdf = MDF(f)
print(mdf.info())
groups_info = {}
for k,v in mdf.info().items():
    print("======")
    # print(k)
    if isinstance(v, dict):
        groups_info[k]=v
        # for sub_k, sub_v in v.items():
        #     print(sub_k, sub_v)
    # else:
    #     print(v)
# for ter in mdf.iter_groups():
#     print(ter)
print(groups_info)
empty_channels = "c"
# 通过mdf.virtual_groups获取到全部的channel group
# 获取该虚拟组中所有的通道

for group_index, (virtual_group_index, virtual_group) in enumerate(mdf.virtual_groups.items()):
    group_channels_idx = []
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
                group_channels_idx.append((None, gp_index, ch_index))
    groups_info[f"group {virtual_group_index}"]['channels_idx'] = group_channels_idx
    print(group_channels_idx)
print(groups_info)

# TODO: 实现全面复制
mdf_copy = MDF()

# 从原来mdf文件复制group和channel(signal)\
for group_name,group_info in groups_info.items():
    # print(group_name)
    # print(group_info)
    group_comment = group_info['comment']
    group_idx = group_info['channels_idx']
    # 获取原来group中的signal
    sigs = []
    for channel_idx in group_idx:
        # print(channel_idx)
        sig = mdf.get(group=channel_idx[1], index=channel_idx[2])
        # 假设sig是一个已经存在的Signal对象
        new_sig = asammdf.Signal(
            samples=sig.samples,
            timestamps=sig.timestamps,
            name=sig.name,
            unit=sig.unit,
            conversion=sig.conversion,  # 复制转换字典
            comment=sig.comment
        )
        print(new_sig)
        print(new_sig)
        new_sig.encoding = 'utf-8'
        # if channel_idx[2]==8:

        # print(signal)
        sigs.append(copy.deepcopy(sig))
        # sigs.append(copy.deepcopy(new_sig))
    mdf_copy.append(sigs,comment=group_comment)

print("copy after...")
for group_index, (virtual_group_index, virtual_group) in enumerate(mdf_copy.virtual_groups.items()):
    group_channels_idx = []
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
                group_channels_idx.append((None, gp_index, ch_index))
    groups_info[f"group {virtual_group_index}"]['channels_idx'] = group_channels_idx
    print(group_channels_idx)

mdf_copy.save('./input/demo_copy.mf4', overwrite=True)

print("复制成功")
# mdf1_copy = mdf.copy()
print(mdf.info())
print(mdf_copy.info())
# print(mdf1_copy.info())
# 存在不一样的根本原因：
# 使用mdf.get()方法获取Signal对象时，返回的Signal对象没有转换字典，可能是因为ASAM MDF文件中没有存储转换字典信息，或者存储的信息不完整。在这种情况下，可以通过其他方式手动添加转换字典。
# TODO:导致后续 concatenate 会有问题！
print("对比验证")

for group_name,group_info in groups_info.items():
    # print(group_name)
    # print(group_info)
    group_comment = group_info['comment']
    group_idx = group_info['channels_idx']
    # 获取原来group中的signal
    sigs = []
    for channel_idx in group_idx:
        # print(channel_idx)
        print("==============")
        sig = str(mdf.get(group=channel_idx[1], index=channel_idx[2]))
        sig_copy = str(mdf_copy.get(group=channel_idx[1], index=channel_idx[2]))
        # print(sig)
        # print(sig_copy)
        if sig==sig_copy:
            print("same")
        else:
            print(sig)
            print(sig_copy)
