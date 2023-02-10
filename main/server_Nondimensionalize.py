"""
无量钢化封装
"""
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import StandardScaler


# 归一化
def _MinMaxScaler(model_train, test_train, feature_range):
    transfer1 = MinMaxScaler(feature_range=feature_range)
    model_train = transfer1.fit_transform(model_train)
    test_train = transfer1.transform(test_train)
    return model_train, test_train, transfer1


# 标准化
def _StandardScaler(model_train, test_train):
    transfer1 = StandardScaler()
    model_train = transfer1.fit_transform(model_train)
    test_train = transfer1.transform(test_train)
    return model_train, test_train, transfer1


def Nondimensionalize(train_type, model_train, test_train, feature_range=(0, 1)):
    if train_type == 0:
        return _StandardScaler(model_train, test_train)
    else:
        return _MinMaxScaler(model_train, test_train, feature_range=feature_range)
