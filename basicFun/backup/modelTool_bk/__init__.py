## dengke.wu@author
from .predictor import MBModel
from maskrcnn_benchmark.config import cfg


class modelTool:

    # 通过config文件和模型文件对maskrcnn-benchmark的模型初始化
    # initModel用于初始化模型
    # cfg_path是model_config.yaml的路径
    # wts_path是模型.pth存放的路径
    def initModel(self, cfg_path, wts_path, labelmap=None):
        cfg.merge_from_file(cfg_path)
        cfg.merge_from_list(["MODEL.WEIGHT", wts_path])
        model = MBModel(cfg)
        if labelmap is not None:
            assert isinstance(labelmap, dict)
            # assert len(labelmap) >= cfg.MODEL.ROI_BOX_HEAD.NUM_CLASSES - 1,
            labelmap = ['__background'] + [v for i, v in labelmap.items() if i > 0]  # convert dict to list
            model.set_categories(labelmap)
        else:
            model.set_categories(None)
        self.model = model
    # 功能：输入一张opencv读取的图片，通过模型返回相应的结果
    # 输入：
    # image为cv读取的图片
    # thresh为置信的阈值
    # 返回值：满足大于阈值的labels、xmin、ymin、xmax、ymax的list（其中坐标且为相对值）
    def getInfoByModel(self, image, thresh=0.7):
        predictions = self.model.compute_prediction(image)
        top_predictions = self.model.select_top_predictions(predictions, thresh)
        normalized_top_predictions = top_predictions.resize((1, 1))
        top_scores = normalized_top_predictions.get_field('scores').numpy()
        top_labels_indexes = normalized_top_predictions.get_field('labels').tolist()
        if self.model.CATEGORIES is not None:
            total_classes = len(self.model.CATEGORIES)
            top_labels = [self.model.CATEGORIES[i] if i < total_classes and i > 0 else str(i) for i in
                          top_labels_indexes]
        else:
            top_labels = top_labels_indexes.numpy()
        top_xmin, top_ymin, top_xmax, top_ymax = normalized_top_predictions.bbox.t().numpy()
        return top_labels, top_xmin, top_ymin, top_xmax, top_ymax, top_scores
