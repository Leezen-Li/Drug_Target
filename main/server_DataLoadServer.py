"""
测试、训练数据获取
"""
import copy
import random

import numpy as np


# 酶数据获取 e
def _e_data_load():
    # 获取相互作用的关联表
    admat_dgc = np.loadtxt('../data/e_admat_dgc.txt', dtype=str, delimiter='\t')
    # 蛋白
    admat_dc = np.loadtxt('../data/e_simmat_dc.txt', dtype=str, delimiter='\t')
    # 药物
    admat_dg = np.loadtxt('../data/e_simmat_dg.txt', dtype=str, delimiter='\t')

    return _common(admat_dgc, admat_dc, admat_dg)


# 离子通道 ic
def _ic_data_load():
    # 获取相互作用的关联表
    admat_dgc = np.loadtxt('../data/ic_admat_dgc.txt', dtype=str, delimiter='\t')
    # 蛋白
    admat_dc = np.loadtxt('../data/ic_simmat_dc.txt', dtype=str, delimiter='\t')
    # 药物
    admat_dg = np.loadtxt('../data/ic_simmat_dg.txt', dtype=str, delimiter='\t')
    return _common(admat_dgc, admat_dc, admat_dg)


# G蛋白偶联受体
def _gpcr_data_load():
    # 获取相互作用的关联表
    admat_dgc = np.loadtxt('../data/gpcr_admat_dgc.txt', dtype=str, delimiter='\t')
    # 蛋白
    admat_dc = np.loadtxt('../data/gpcr_simmat_dc.txt', dtype=str, delimiter='\t')
    # 药物
    admat_dg = np.loadtxt('../data/gpcr_simmat_dg.txt', dtype=str, delimiter='\t')
    return _common(admat_dgc, admat_dc, admat_dg)


# 核受体
def _nr_data_load():
    # 获取相互作用的关联表
    admat_dgc = np.loadtxt('../data/nr_admat_dgc.txt', dtype=str, delimiter='\t')
    # 蛋白
    admat_dc = np.loadtxt('../data/nr_simmat_dc.txt', dtype=str, delimiter='\t')
    # 药物
    admat_dg = np.loadtxt('../data/nr_simmat_dg.txt', dtype=str, delimiter='\t')
    return _common(admat_dgc, admat_dc, admat_dg)


# 获取相同数目的相关与无关数据
def _common(admat_dgc, admat_dc, admat_dg):
    model_train = []
    model_label = []

    admat_dgc = np.delete(admat_dgc, 0, 0)
    admat_dgc = np.delete(admat_dgc, 0, 1)
    admat_dc = np.delete(admat_dc, 0, 0)
    admat_dc = np.delete(admat_dc, 0, 1)
    admat_dg = np.delete(admat_dg, 0, 0)
    admat_dg = np.delete(admat_dg, 0, 1)
    # 获取所有具有相互作用的数据
    i_index = -1
    for i in admat_dgc:
        i_index += 1
        j_index = -1
        for j in i:
            j_index += 1
            if j == '1':
                temp_dg = copy.deepcopy(admat_dg[i_index]).tolist()
                temp_dc = copy.deepcopy(admat_dc[j_index]).tolist()
                temp_dg.extend(temp_dc)
                model_train.append(temp_dg)
                model_label.append(1)

    # 添加相同数量的无相互作用的数据
    x_len = len(admat_dgc) - 1
    y_len = len(admat_dgc[0]) - 1
    data_len = len(model_train)
    only_dist = {}

    for i in range(0, data_len):
        # 获取随机相互作用的x与y
        x = random.randint(0, x_len)
        y = random.randint(0, y_len)

        # 防止重复
        while admat_dgc[x][y] != '0' or only_dist.get(str(x) + '_' + str(y)) is not None:
            x = random.randint(0, x_len)
            y = random.randint(0, y_len)
        only_dist[str(x) + '_' + str(y)] = True

        temp_dg = copy.deepcopy(admat_dg[x]).tolist()
        temp_dc = copy.deepcopy(admat_dc[y]).tolist()
        temp_dg.extend(temp_dc)
        model_train.append(temp_dg)
        model_label.append(0)
    return model_train, model_label


def Data_load(train_type, path=None):
    if train_type == 0:
        return _e_data_load()
    elif train_type == 1:
        return _ic_data_load()
    elif train_type == 2:
        return _gpcr_data_load()
    elif train_type == 3:
        return _nr_data_load()


if __name__ == '__main__':
    model_train, model_label = Data_load(1)
    print(model_train)
    print(model_label)
    #
    # with open("核受体预测数据.txt", 'w+') as fp:
    #     for i in model_train:
    #         flag = False
    #         for j in i:
    #             if flag:
    #                 fp.write("\t")
    #             fp.write(j)
    #             flag = True
    #         fp.write("\n")

    # admat_dgc = np.loadtxt('../data/e_admat_dgc.txt', dtype=str, delimiter='\t')
    # print(admat_dgc)
