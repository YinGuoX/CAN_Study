from asammdf import MDF
import asammdf
import copy
"""
抽取出指定group的数据进行合并，代码合并方式以及concate方式都可行！
"""


f = r"./input/test1.mf4"
mdf = MDF(f)

print(mdf.info())

group0_data = mdf.get_group(index=0)
print(group0_data)
print(type(group0_data))



# 抽取指定group的数据，组成一个新的mdf文件
group_idxs = [0]

with MDF(f) as mdf:
    occurrences = [
        (None, gp_idx, cn_idx)
        for occ in mdf.channels_db.values()
        for gp_idx, cn_idx in occ
        if gp_idx in group_idxs
    ]
    filtered_mdf = mdf.filter(occurrences)

save_file_path = './input/test1_onep.mf4'
save_file_path1 = './input/test1_onep1.mf4'
filtered_mdf.save(save_file_path,overwrite=True)
filtered_mdf.save(save_file_path1,overwrite=True)
test1_onep = MDF(save_file_path)
test1_onep1 = MDF(save_file_path1)


# 两个文件使用concatenate的方式进行拼接
mdf_concat = MDF.concatenate([test1_onep,test1_onep1])
print(mdf_concat.info())
print(mdf_concat.get_group(0))
# 可视化验证拼接效果！
signal = test1_onep.get(group=0,index=0)
signal.plot()
signal = test1_onep1.get(group=0,index=0)
signal.plot()
signal = mdf_concat.get(group=0,index=0)
signal.plot()

# 使用代码的方式进行拼接！
groups_info = {}
for k,v in test1_onep.info().items():
    print("======")
    # print(k)
    if isinstance(v, dict):
        groups_info[k]=v

print(groups_info)
empty_channels = 'e'
for group_index, (virtual_group_index, virtual_group) in enumerate(test1_onep.virtual_groups.items()):
    group_channels_idx = []
    if virtual_group.cycles_nr == 0 and empty_channels == "skip":
        continue
    # mdf.included_channels(virtual_group_index)方法获取到当前channel group下包含的channels
    # 获取的channels是一个元组列表，第一个都是None,第二个和第三个分别是channel group的index和channel的index，
    # mdf.get()方法的参数其实有很多，前三个是signal name，group index，channel index，其实就是列表元组的三个，因为channel group、channel是一个二维结构，所以，其实可以不用信号名来获取信号，也可以通过group index，和channel index，然后第一个参数传None，
    included_channels = test1_onep.included_channels(virtual_group_index)[virtual_group_index]
    for gp_index, channel_indexes in included_channels.items():
        for ch_index in channel_indexes:
            # 排除主通道
            # 在CAN总线中，每个节点都有一个唯一的标识符，称为节点ID。主通道是用于接收和发送节点ID的通道，因此它不应该被视为普通的数据通道。在这段代码中，排除主通道是为了避免将主通道误认为是普通的数据通道，从而导致数据处理错误。
            if ch_index != test1_onep.masters_db.get(gp_index, None):
                group_channels_idx.append((None, gp_index, ch_index))
    groups_info[f"group {virtual_group_index}"]['channels_idx'] = group_channels_idx
    print(group_channels_idx)
print(groups_info)
mdf_ext = MDF()
for group_name,group_info in groups_info.items():
    group_comment = group_info['comment']
    group_idx = group_info['channels_idx']
    ext_sigs = []
    for channel_idx in group_idx:
        # 获取原来group中的signal
        sig_ori = test1_onep.get(group=channel_idx[1], index=channel_idx[2])
        sig_ori2 = test1_onep1.get(group=channel_idx[1], index=channel_idx[2])
        extend_sig = sig_ori2.extend(sig_ori)
        ext_sigs.append(copy.deepcopy(extend_sig))
    mdf_ext.append(ext_sigs, comment=group_comment)
print(mdf_ext.info())
signal = mdf_ext.get(group=0,index=0)
signal.plot()


