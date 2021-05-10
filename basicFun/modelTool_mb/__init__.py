## dengke.wu@author
from .predictor import MBModel
from maskrcnn_benchmark.config import cfg
import numpy as np

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
    def nms_exclusive_boxes(self,boxes,classes,exclusiveGroups,thresh,specialThresh):
        def match_boxes(preBoxes,preClasses,thresh,specialThresh):
            def get_iou(box1, box2):
                """
                :param box1:[x1,y1,x2,y2] 左上角的坐标与右下角的坐标
                :param box2:[x1,y1,x2,y2]
                :return: iou_ratio--交并比
                """
                # box1=[int(obj1['xmin']),int(obj1['ymin']),int(obj1['xmax']),int(obj1['ymax'])]
                # box2=[int(obj2['xmin']),int(obj2['ymin']),int(obj2['xmax']),int(obj2['ymax'])]
                width1 = abs(box1[2] - box1[0])
                height1 = abs(box1[1] - box1[3])  # 这里y1-y2是因为一般情况y1>y2，为了方便采用绝对值
                width2 = abs(box2[2] - box2[0])
                height2 = abs(box2[1] - box2[3])
                x_max = max(box1[0], box1[2], box2[0], box2[2])
                y_max = max(box1[1], box1[3], box2[1], box2[3])
                x_min = min(box1[0], box1[2], box2[0], box2[2])
                y_min = min(box1[1], box1[3], box2[1], box2[3])
                iou_width = x_min + width1 + width2 - x_max
                iou_height = y_min + height1 + height2 - y_max
                if iou_width <= 0 or iou_height <= 0:
                    iou_ratio = 0
                else:
                    iou_area = iou_width * iou_height  # 交集的面积
                    box1_area = width1 * height1
                    box2_area = width2 * height2
                    iou_ratio = iou_area / (box1_area + box2_area - iou_area)  # 并集的面积
                return iou_ratio
            postBoxes=[]
            postClasses=[]
            usedBoxes=[]
            for i, preBox in enumerate(preBoxes):
                used=0
                for usedBox in usedBoxes:
                    if all(preBox==usedBox):
                        used=1
                if used==0:
                    usedBoxes.append(preBox)
                    matchBox=preBox
                    matchClass=preClasses[i]
                    maxMatchScore=preBox[4]
                    matchScore=preBox[4]
                    for p, pBox in enumerate(preBoxes[i+1:]):
                        pused=0
                        for usedBox in usedBoxes:
                            if all(pBox==usedBox):
                                pused=1
                        if pused==0:
                            boxIou=get_iou(preBox[:4],pBox[:4])
                            if boxIou>0.7:
                                usedBoxes.append(pBox)
                                matchScore+=pBox[4]
                                if pBox[4]>maxMatchScore:
                                    maxMatchScore=pBox[4]
                                    matchBox=pBox
                                    matchClass=preClasses[p+i+1]
                    matchBox[4]=min(matchScore,1.0)
                    if self.model.CATEGORIES[matchClass] in specialThresh.keys():
                        cthresh=specialThresh[self.model.CATEGORIES[matchClass]]
                    else:
                        cthresh=thresh
                    if matchBox[4]>cthresh:
                        postBoxes.append(matchBox)
                        postClasses.append(matchClass)
            return postBoxes,postClasses
        preBoxes=[]
        preClasses=[]
        try:
            for i, c in enumerate(classes):
                for exclusiveGroup in exclusiveGroups:
                    if self.model.CATEGORIES[c] in specialThresh.keys():
                        cthresh=specialThresh[self.model.CATEGORIES[c]]
                    else:
                        cthresh=thresh
                    if self.model.CATEGORIES[c] in exclusiveGroup:
                        shareThresh=cthresh/len(exclusiveGroup)
                        if boxes[i][4]>shareThresh:
                            preBoxes.append(boxes[i])
                            preClasses.append(c)
                        break
                if boxes[i][4]>cthresh:
                    preBoxes.append(boxes[i])
                    preClasses.append(c)
        except:
            pass
        postBoxes,postClasses=match_boxes(preBoxes,preClasses,thresh,specialThresh)
        return postBoxes,postClasses
    def getInfoByModel(self, image, thresh=0.7):
        predictions = self.model.compute_prediction(image)
        top_predictions=predictions
        normalized_top_predictions = top_predictions.resize((1, 1))
        top_scores = normalized_top_predictions.get_field('scores').numpy()
        top_labels_indexes = normalized_top_predictions.get_field('labels').tolist()
        top_xmin, top_ymin, top_xmax, top_ymax = normalized_top_predictions.bbox.t().numpy()
        exclusiveGroups=[['truck','car','tanker','bus','motorcycle'],['blue','yellow','red','gray','security','other']]
        specialThresh = {'sdf':0.6,'def':0.6}
        boxes=[]
        for i in range(len(top_scores)):
            box=np.array([top_xmin[i],top_ymin[i],top_xmax[i],top_ymax[i],top_scores[i]])
            boxes.append(box)
        boxes,classes=self.nms_exclusive_boxes(boxes,top_labels_indexes,exclusiveGroups,thresh,specialThresh)
        top_labels=[]
        top_xmin=[]
        top_ymin=[]
        top_xmax=[]
        top_ymax=[]
        top_scores=[]
        try:
            for i, box in enumerate(boxes):
                top_labels.append(self.model.CATEGORIES[classes[i]])
                top_xmin.append(float(box[0]))
                top_ymin.append(float(box[1]))
                top_xmax.append(float(box[2]))
                top_ymax.append(float(box[3]))
                top_scores.append(box[4])
        except:
            pass
        return top_labels,top_xmin,top_ymin,top_xmax,top_ymax,top_scores
