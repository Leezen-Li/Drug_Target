import json
import shutil
import threading
from time import time

from domain_ModelData import ModelData as ModelDataClass
# from domain_Data import Data as DataClass
from server_DataLoadServer import *
from server_DimensionReduction import *
from server_Nondimensionalize import *
from server_TrainAlgorithm import *

from sklearn.model_selection import train_test_split
from domain_Data import *


class TrainThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, param_data):
        threading.Thread.__init__(self)
        self.param_data = param_data
        self.info_list = Data.info_list

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        param_data = self.param_data
        try:
            # 数据获取
            model_train, model_label = Data_load(param_data.get("model_type"))

            # 特征降维
            transfer1 = None
            # 特征降维
            if param_data.get("isDimensionReduction"):
                if param_data.get("dimensionReductionType") == 0:
                    model_train, transfer1 = DimensionReduction(0, model_train,
                                                                n_components=param_data.get("pca_components"))
                else:
                    model_train, transfer1 = DimensionReduction(1, model_train,
                                                                param_threshold=param_data.get("threshold"))

            # 数据划分
            model_train, test_train, model_label, test_label = train_test_split(model_train, model_label)

            transfer2 = None
            # 无量纲化
            if param_data.get("isNondimensionalize"):
                if param_data.get("nondimensionalizeType") == 0:
                    model_train, test_train, transfer2 = Nondimensionalize(0, model_train, test_train)
                else:
                    model_train, test_train, transfer2 = Nondimensionalize(1, model_train, test_train,
                                                                           param_data.get("feature_range"))

            # 预估器获取
            estimator = TrainAlgorithm(param_data.get("estimatorType"), model_train, model_label, param_obj=param_data)

            predict = estimator.predict(test_train)
            # print(estimator.best_params_)

            score = estimator.score(test_train, test_label)
            param_data["accuracy"] = score

            # 精确率与召回率
            from sklearn.metrics import classification_report

            # 获取召回率之类的
            report = classification_report(test_label, predict, labels=[0, 1],
                                           target_names=["无相互作用", "有相互作用"],
                                           output_dict=True)
            param_data["report"] = report

            from sklearn.metrics import roc_auc_score

            AUC = roc_auc_score(test_label, predict)
            param_data["AUC"] = AUC

            param_data["time"] = time()
            save_model(param_data.get("model_type"), transfer1, transfer2, estimator, param_data)

            # 处理之后回调表示完毕，之后获取数据
            # self.win.calljs('window.store.commit("flushModelInfoList")')

            self.info_list.append(
                {'state': 0, 'title': '模型训练', 'message': '模型' + param_data['model_name'] + '训练完毕'})
        except Exception:
            print("训练失败")
            self.info_list.append(
                {'state': 1, 'title': '模型训练',
                 'message': '模型' + param_data['model_name'] + '训练失败，请检查训练参数是否正确'})


class DeleteThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, param_data):
        threading.Thread.__init__(self)
        self.param_data = param_data

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        save_path = ""

        if self.param_data.get("model_type") == 0:
            save_path = "../model/E/"
        elif self.param_data.get("model_type") == 1:
            save_path = "../model/IC/"
        elif self.param_data.get("model_type") == 2:
            save_path = "../model/GPCR/"
        elif self.param_data.get("model_type") == 3:
            save_path = "../model/NR/"
        print(save_path + self.param_data.get("file_name"))

        shutil.rmtree(save_path + self.param_data.get("file_name"))

        Data.info_list.append(
            {'state': 0, 'title': '模型删除',
             'message': '模型' + self.param_data['file_name'] + '删除完毕'})


class PredictThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, predict_config_str):
        threading.Thread.__init__(self)
        self.predict_config_str = predict_config_str

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        predict_config = json.loads(self.predict_config_str)
        try:
            print(predict_config)
            if predict_config.get("predict_data_path") is None or predict_config.get(
                    "model_type") is None or predict_config.get("model_name") is None or predict_config.get(
                "file_name") is None:
                return "参数出错"

            param_data = predict_config

            predict_data = np.loadtxt(param_data.get("predict_data_path"), dtype=str, delimiter='\t')
            save_path = ""
            if param_data.get("model_type") == 0:
                save_path = "../model/E/"
            elif param_data.get("model_type") == 1:
                save_path = "../model/IC/"
            elif param_data.get("model_type") == 2:
                save_path = "../model/GPCR/"
            elif param_data.get("model_type") == 3:
                save_path = "../model/NR/"

            path = save_path + param_data.get("model_name")

            with open(path + '/param_data', 'rb') as fp:
                params = pickle.load(fp)

            # 降维
            if params.get("isDimensionReduction"):
                with open(path + '/transfer1', 'rb') as fp:
                    transfer1 = pickle.load(fp)
            # 无量纲化
            if params.get("isNondimensionalize"):
                with open(path + '/transfer2', 'rb') as fp:
                    transfer2 = pickle.load(fp)
            with open(path + '/estimator', 'rb') as fp:
                estimator = pickle.load(fp)

            predict_data = transfer1.transform(predict_data)
            predict_data = transfer2.transform(predict_data)
            result = estimator.predict(predict_data)

            save_predict_result(result, file_name=param_data.get("file_name"))

            Data.info_list.append(
                {'state': 0, 'title': '模型预测',
                 'message': '模型预测完毕，预测结果请在主目录的predict文件夹查看'})
        except:
            print("有问题")
            Data.info_list.append(
                {'state': 1, 'title': '模型预测',
                 'message': '请检查预测文件格式是否正确，以及预测类型是否对应'})
