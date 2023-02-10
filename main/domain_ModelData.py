"""
用于模型数据保存

"""
import configparser
import json
import pickle


class ModelData(dict):
    def __init__(self):
        # 模型名称
        self["id"] = None
        self["model_name"] = None

        # 0 1 2 3 4
        # 酶、离子通道、G蛋白偶联受体、核受体、自己的数据
        self["model_type"] = 0

        # 是否采用无量纲化【默认采用】
        self["isNondimensionalize"] = True
        # 无量纲化方法【0为标准化、1为归一化】【默认为标准化】
        self["nondimensionalizeType"] = 0
        # 归一化范围：
        self["feature_range"] = (0, 1)

        # 是否采用降维
        self["isDimensionReduction"] = True
        # 采用降维的方法  【0为PCA  1为方差选择 2相关系数有待考量】
        self["dimensionReductionType"] = 0
        # 数据保留比例或者减少到多少特征【默认百分之95】
        self["pca_components"] = 0.90
        # 方差选择的阈值【默认为0】
        self["threshold"] = 0

        # 预估器的方法为 【0 KNN算法 1 朴素贝叶斯 2决策树 3随机森林】
        self["estimatorType"] = 0

        # KNN相近数量 【默认为5】
        self["n_neighbors"] = [1, 2, 3, 4, 5]

        # 朴素贝叶斯 【拉普拉斯平滑系数 默认1.0】
        self["alpha"] = 1.0

        # 决策树 【不纯度 默认基尼系数 可以配置信息熵 entropy】
        self["criterion"] = 'gini'
        # 最大深度
        self["max_depth"] = None
        # 随机数种子
        self["random"] = None

        # 决策森林【森林中数目的数量】
        self["n_estimators"] = [9, 10, 11, 12, 13, 14, 15]

        # 【不纯度 决策树划分依据 默认基尼系数 可以配置信息熵 entropy】
        self["forest_criteria"] = 'gini'
        # 最大深度
        self["forest_max_depth"] = None
        # 是否放回抽取
        self["forest_bootstrap"] = True
        #  后续暂时放置【因为不知道默认配置】

        # 精确率、召回率、F1-score指标、AUC指标、交叉验证折数、准确率
        # 模型准确率
        self["accuracy"] = None
        # 精确率、召回率、F1-score指标
        self["report"] = None
        # AUC指标
        self["AUC"] = None
