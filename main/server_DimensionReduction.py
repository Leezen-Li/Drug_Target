"""
降维对象封装
"""
from sklearn.decomposition import PCA
from sklearn.feature_selection import VarianceThreshold


def _PCA(model_train, param_n_components):
    transfer = PCA(n_components=param_n_components)
    model_train = transfer.fit_transform(model_train)
    return model_train, transfer


def _Threshold(model_train, param_threshold):
    transfer = VarianceThreshold(threshold=param_threshold)
    model_train = transfer.fit_transform(model_train)
    return model_train, transfer


def DimensionReduction(dr_type, model_train, n_components=None, param_threshold=0.0):
    if dr_type == 0:
        return _PCA(model_train=model_train, param_n_components=n_components)
    else:
        return _Threshold(model_train, param_threshold)
