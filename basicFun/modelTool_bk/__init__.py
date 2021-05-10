#coding: utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from collections import defaultdict
import argparse
import cv2  # NOQA (Must import before importing caffe2 due to bug in cv2)
import glob
import logging
import os
import sys
import time

from caffe2.python import workspace

from detectron.core.config import assert_and_infer_cfg
from detectron.core.config import cfg
from detectron.core.config import merge_cfg_from_file
from detectron.utils.timer import Timer
import detectron.core.test_engine as infer_engine
import detectron.datasets.dummy_datasets as dummy_datasets
import detectron.utils.c2 as c2_utils
import detectron.utils.logging
import detectron.utils.vis as vis_utils
# import  detectron.core.test as infer_engine
c2_utils.import_detectron_ops()

workspace.GlobalInit(['caffe2', '--caffe2_log_level=0'])
workspace.SwitchWorkspace("bxg",True)
class modelTool:
    def __init__(self):
        pass

    # 通过config文件和模型文件对caffe2的模型初始化
    # initModel用于初始化模型
    # cfg_path是model_config.yaml的路径
    # wts_path是模型.pkl存放的路径
    def initModel(self,cfg_path,wts_path,labelmap):
        merge_cfg_from_file(cfg_path)
        # cfg.TEST.WEIGHTS = wts_path
        cfg.NUM_GPUS = 1
        assert_and_infer_cfg()
        self.labelmap = labelmap
        self.model = infer_engine.initialize_model_from_cfg(wts_path)
        
    # def __del__(self):
    #     try:
    #         while True:
    #             del self
    #     except:
    #         pass

    # 功能：输入一张opencv读取的图片，通过模型返回相应的结果
    # 输入：
    # image为cv读取的图片
    # thresh为置信的阈值
    # 返回值：满足大于阈值的labels、xmin、ymin、xmax、ymax的list（其中坐标且为相对值）
    def getInfoByModel(self,image,thresh=0.7):
        top_labels = []
        top_xmin = []
        top_ymin = []
        top_xmax = []
        top_ymax = []
        top_scores = []
        timers = defaultdict(Timer)
        # with c2_utils.NamedCudaScope(0):
        #     cls_boxes, cls_segms, cls_keyps = infer_engine.im_detect_all(
        #     self.model, image, None, timers=timers
        #     )
        with c2_utils.NamedCudaScope(0):
            cls_boxes, cls_segms, cls_keyps = infer_engine.im_detect_all(
            self.model, image, None, timers=timers
            )    
        boxes, segms, keypoints, classes = vis_utils.convert_from_cls_format(cls_boxes, cls_segms, cls_keyps)
        specific_thresh = {'sdf':0.6,'def':0.6}
        try:
            for i, box in enumerate(boxes):
                # print(box)
                temp_thresh = thresh
                if self.labelmap[classes[i]] in specific_thresh:
                    temp_thresh = specific_thresh[self.labelmap[classes[i]]]
                if box[-1] > temp_thresh:
                    try:
                        top_labels.append(self.labelmap[classes[i]])
                    except:
                        top_labels.append(str(classes[i]))
                    # print(classes)
                    # print(self.labelmap[classes[i]])
                    top_xmin.append(float(box[0])/float(image.shape[1]))
                    top_ymin.append(float(box[1])/float(image.shape[0]))
                    top_xmax.append(float(box[2])/float(image.shape[1]))
                    top_ymax.append(float(box[3])/float(image.shape[0]))
                    top_scores.append(box[4])
        except:
            pass
        return top_labels,top_xmin,top_ymin,top_xmax,top_ymax,top_scores
    def getKptByModel(self,image,thresh=0.7):
        top_labels = []
        top_xmin = []
        top_ymin = []
        top_xmax = []
        top_ymax = []
        top_scores = []
        timers = defaultdict(Timer)
        # with c2_utils.NamedCudaScope(0):
        #     cls_boxes, cls_segms, cls_keyps = infer_engine.im_detect_all(
        #     self.model, image, None, timers=timers
        #     )
        with c2_utils.NamedCudaScope(0):
            cls_boxes, cls_segms, cls_keyps= infer_engine.im_detect_all(
            self.model, image, None, timers=timers
            ) 
        # boxes, segms, keypoints, classes = vis_utils.convert_from_cls_format(cls_boxes, cls_segms, cls_keyps)
        image=vis_utils.vis_one_image_opencv(
            image,
            cls_boxes,
            cls_segms,
            cls_keyps,
            dataset=None,
            show_class=True,
            thresh=0.7,
            kp_thresh=2
        )
        # try:
        #     print (keypoints)
        # except:
        #     pass
        return image

    # 功能：输入一张opencv读取的图片，通过模型返回相应的结果
    # 输入：
    # image为cv读取的图片
    # thresh为置信的阈值
    # 返回值：box（xmin,ymin,xmax,ymax,score） class为labels的list（此处的坐标为照片中的真实数值）
    def getInfoByModel_orig(self,image,thresh=0.6):
        timers = defaultdict(Timer)
        with c2_utils.NamedCudaScope(0):
            cls_boxes, cls_segms, cls_keyps = infer_engine.im_detect_all(
            self.model, image, None, timers=timers
            )
        boxes, segms, keypoints, classes = vis_utils.convert_from_cls_format(cls_boxes, cls_segms, cls_keyps)
        boxes_top = []
        classes_top = []
        if boxes is not None:
            for i, box in enumerate(boxes):
                if box[-1] > thresh:
                    boxes_top.append(box)
                    classes_top.append(self.labelmap[classes[i]])
        return boxes_top,classes_top

    # 功能：输入一张opencv读取的图片，已经满足阈值的相关信息，以及画图所需要的资源 
    # 输入：
    # image为cv读取的图片
    # boxes_top（xmin,ymin,xmax,ymax,score） classes_top为labels的list(两者是已经满足阈值的list)
    # category_dict 为类别（1，2，....）所对应的标签，类型为字典
    # colors_tableau 颜色list
    # font opencv的字体
    # 返回：一张标注完成的cv_array
    def visImage(self,image,boxes_top,classes_top,category_dict,colors_tableau,font):
        for i, box in enumerate(boxes_top):
            xmin = int(round(box[0]))
            ymin = int(round(box[1]))
            xmax = int(round(box[2]))
            ymax = int(round(box[3]))
            #print("xmin = %d\tymin = %d\t xmax = %d\t ymax = %d\t score = %0.2f"%(xmin,ymin,xmax,ymax,box[4]))
            color = colors_tableau[classes_top[i]]
            cv2.rectangle(image, (xmin, ymin), (xmax, ymin+25), (201, 252, 189), thickness=-1)
            cv2.rectangle(image, (xmin, ymin) ,(xmax,ymax), color, 2)
            print(category_dict)
            cv2.putText(image, ' ' + category_dict[classes_top[i]]+' %0.2f'%(box[-1]), (xmin,ymin+18) , font , 0.6 , (205,90,106) , 2)
        return image










