"""
配置初始化、
数据的读取

以防出现错误、一般先直接获取对象的多少、配置文件ini的读取

以及数据更新之后的改变和保存
"""
import copy
import os
import uuid
import pickle
from queue import Queue

from openpyxl import Workbook


class Data(dict):
    info_list = []
    current_info = ""
    model_info = {
        'E': {},
        'IC': {},
        'GPCR': {},
        'NR': {}
    }

    def flushInfo(self):
        if len(self.info_list) != 0:
            Data.current_info = Data.info_list.pop(0)
        else:
            Data.current_info = {'state': -1}

    def load_models(self):
        dir_list = ["../model/E/", "../model/IC/", "../model/GPCR/", "../model/NR/"]
        Data.model_info = {
            'E': {},
            'IC': {},
            'GPCR': {},
            'NR': {}
        }
        flag = 0
        for dir_path in dir_list:
            flag += 1
            dirs = os.listdir(dir_path)

            for dir in dirs:
                with open(dir_path + dir + "/" + "param_data", 'rb') as fp:
                    param_data = pickle.load(fp)
                if flag == 1:
                    Data.model_info["E"][dir] = param_data
                elif flag == 2:
                    Data.model_info["IC"][dir] = param_data
                elif flag == 3:
                    Data.model_info["GPCR"][dir] = param_data
                elif flag == 4:
                    Data.model_info["NR"][dir] = param_data
        print(Data.model_info)

    def load_log(self):
        print("预测结果获取")

    def save_log(self):
        print("模型训练之后保存记录")

    def get_log(self):
        print("前端你直接数据请求后返回")

    #
    # if __name__ == '__main__':
    #     # data = Data()
    #     load_models()


def save_model(model_type, transfer1, transfer2, estimator, param_data):
    # 存储模型类型
    if model_type == 0:
        save_path = "../model/E/"
    elif model_type == 1:
        save_path = "../model/IC/"
    elif model_type == 2:
        save_path = "../model/GPCR/"
    elif model_type == 3:
        save_path = "../model/NR/"

    # 模型id获取
    model_id = str(uuid.uuid4())
    param_data["id"] = model_id
    dir_path = save_path + param_data["model_name"] + "-" + model_id + "/"

    # 创建路劲
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    # 模型保存
    with open(dir_path + "estimator", 'wb') as fp:
        pickle.dump(estimator, fp)
    with open(dir_path + "param_data", 'wb') as fp:
        pickle.dump(param_data, fp)

    if transfer1 is not None:
        with open(dir_path + "transfer1", 'wb') as fp:
            pickle.dump(transfer1, fp)
    if transfer2 is not None:
        with open(dir_path + "transfer2", 'wb') as fp:
            pickle.dump(transfer2, fp)

    return model_id


def save_predict_result(predict_data, file_name):
    predict_data = predict_data.tolist()
    wb = Workbook()
    # 获取被激活的 worksheet
    ws = wb.active
    # 设置单元格内容
    ws.append(predict_data)

    wb.save("../predict/"+file_name+'.xlsx')
