from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


# KNN算法
def _KNN(model_train, model_label, n_neighbors_param=[1, 3, 5, 7, 9]):
    estimator = KNeighborsClassifier()
    params = {'n_neighbors': n_neighbors_param}
    estimator = GridSearchCV(estimator=estimator, param_grid=params, cv=10)
    estimator.fit(model_train, model_label)
    return estimator


# 朴素贝叶斯算法
def _Bayes(model_train, model_label, param_alpha=1.0):
    estimator = MultinomialNB(alpha=param_alpha)
    params = {}
    estimator = GridSearchCV(estimator=estimator, param_grid=params, cv=10)
    estimator.fit(model_train, model_label)
    return estimator


# 决策树
def _DecisionTree(model_train, model_label, param_criterion='gini', param_max_depth=None, param_random=None):
    estimator = DecisionTreeClassifier(criterion=param_criterion, max_depth=param_max_depth, random_state=param_random)

    params = {}
    estimator = GridSearchCV(estimator=estimator, param_grid=params, cv=10)

    estimator.fit(model_train, model_label)
    return estimator


# 随机森林
def _Forest(model_train, model_label, param_n_estimators=[9, 10, 11, 12, 13, 14, 15], param_criterion='gini',
            param_max_depth=None,
            param_bootstrap=True):
    estimator = RandomForestClassifier(criterion=param_criterion, max_depth=param_max_depth, bootstrap=param_bootstrap)

    params = {'n_estimators': param_n_estimators}
    estimator = GridSearchCV(estimator=estimator, param_grid=params, cv=10)

    estimator.fit(model_train, model_label)
    return estimator


def TrainAlgorithm(train_type, model_train, model_label, param_obj):
    if train_type == 0:
        return _KNN(model_train, model_label, param_obj.get("n_neighbors"))
    elif train_type == 1:
        return _Bayes(model_train, model_label, param_obj.get("alpha"))
    elif train_type == 2:
        return _DecisionTree(model_train, model_label, param_obj.get("criterion"), param_obj.get("max_depth"),
                             param_obj.get("random_state"))
    elif train_type == 3:
        return _Forest(model_train, model_label, param_obj.get("n_estimators"), param_obj.get("forest_criteria"),
                       param_obj.get("forest_max_depth"),
                       param_obj.get("bootstrap"))
