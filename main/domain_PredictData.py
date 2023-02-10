# 预测结果与储存分开
# 预测结果保存->预测的模型参数、预测的结果
class PredictData(dict):
    def __init__(self):
        super().__init__()
        self["predict_data_path"] = None
        # 模型参数
        self["model_type"] = None
        # 模型名称
        self["model_name"] = None
        # 文件数据文件保存名称
        self["file_name"] = None
