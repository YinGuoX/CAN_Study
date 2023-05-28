from asammdf import MDF
import copy
"""
将mf4格式 复制后 使用 合并信号的方式 合并数据 =>因为没有删除信号的方法，所以只能使用重新写入一个新的mdf文件的方式来做了！
"""


# f = r"./input/demo.mf4"
f = r"./input/Acceleration_StandingStart.mf4"
# f1 = r"./input/demo_shou.mf4"
f1 = r"./input/Acceleration_StandingStart.mf4"
mdf = MDF(f)
mdf_copy = MDF(f1)
print(mdf.info())
print(mdf_copy.info())

groups_info = {}
for k,v in mdf.info().items():
    print("======")
    # print(k)
    if isinstance(v, dict):
        groups_info[k]=v

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
mdf_ext = MDF()
for group_name,group_info in groups_info.items():
    group_comment = group_info['comment']
    group_idx = group_info['channels_idx']
    ext_sigs = []
    for channel_idx in group_idx:
        # 获取原来group中的signal
        sig_ori = mdf.get(group=channel_idx[1], index=channel_idx[2])
        sig_ori2 = mdf_copy.get(group=channel_idx[1], index=channel_idx[2])
        extend_sig = sig_ori2.extend(sig_ori)
        ext_sigs.append(copy.deepcopy(extend_sig))
    mdf_ext.append(ext_sigs, comment=group_comment)
print("复制成功")
# mdf1_copy = mdf.copy()
print(mdf.info())
print(mdf_ext.info())
signal = mdf.get(group=0,index=0)
signal_ext = mdf_ext.get(group=0,index=0)
signal.plot()
signal_ext.plot()

