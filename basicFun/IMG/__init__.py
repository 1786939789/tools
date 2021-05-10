import os
from PIL import Image
import cv2
import numpy as np
def img_cos_for_labels(basePath, checkPath, baseRoi=[],checkRoi=[]):
    baseRoi=cut_roi_for_labels(basePath,baseRoi)
    checkRoi=cut_roi_for_labels(checkPath,checkRoi)
    baseGray=rgb2gray(baseRoi)
    checkGray=rgb2gray(checkRoi)
    return cos(gray2array_ave(baseGray),gray2array_ave(checkGray))
def compare_cos_featrue(basePath, checkPath, roi=[]):
    baseRoi=cut_roi(basePath,roi)
    checkRoi=cut_roi(checkPath,roi)
    baseGray=rgb2gray(baseRoi)
    checkGray=rgb2gray(checkRoi)
    return cos(gray2array_ave(baseGray),gray2array_ave(checkGray))
def compare_LBP_featrue(basePath, checkPath, roi):
    baseRoi=cut_roi(basePath,roi)
    checkRoi=cut_roi(checkPath,roi)
    baseFeatrue=get_LBP_featrue(baseRoi)
    checkFeatrue=get_LBP_featrue(checkRoi)
    return cos(gray2array_ave(baseFeatrue),gray2array_ave(checkFeatrue))
def cos(baseArray,checkArray):
    num=np.dot(baseArray,checkArray)
    denom=np.linalg.norm(baseArray)*np.linalg.norm(checkArray)
    cosValue=num/denom
    return cosValue
def cut_roi(jpgPath,roi=(100,100,200,200)):
    # roi=(int(xmin),int(ymin),int(xmax),int(ymax))
    img=Image.open(jpgPath)
    if roi!=[]:
        try:
            img=img.crop(roi)
            if roi[3]-roi[1]>200:
                img=img.resize((128,64),Image.ANTIALIAS)
        except:
            print("Wrong roi")
            return None
    else:
        baseImg = cv2.imread(jpgPath)
        # img=cv2.resize(baseImg,(256, 256))
        img=cv2.resize(baseImg,(128, 64))
    # img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
    return img
def cut_roi_for_labels(jpgPath,roi=(100,100,200,200)):
    # roi=(int(xmin),int(ymin),int(xmax),int(ymax))
    img=Image.open(jpgPath)
    if roi!=[]:
        try:
            img=img.crop(roi)
            img=img.resize((64,64),Image.ANTIALIAS)
        except:
            print("Wrong roi")
            return None
    else:
        baseImg = cv2.imread(jpgPath)
        # img=cv2.resize(baseImg,(256, 256))
        img=cv2.resize(baseImg,(64, 64))
    # img = cv2.cvtColor(np.asarray(img),cv2.COLOR_RGB2BGR)
    return img
def save_image(imgPath,region):
    region.save(imgPath,"jpeg")
def get_LBP_featrue(rgb):
    gray=rgb2gray(rgb)
    img_feature = np.zeros(gray.shape,np.uint8) 
    H,W=gray.shape
    for h in range(H):
        for w in range(W):
            ## h-1,w-1
            Sum=0
            if h==0 or w==0:
                Sum+=0
            else:
                Sum+=(gray[h-1,w-1] > gray[h,w])
            ## h-1,w
            if h==0:
                Sum*=2
            else:
                Sum*=2
                Sum+=(gray[h-1,w] > gray[h,w])
            ## h-1,w+1
            if h==0 or w==W-1:
                Sum*=2
            else:
                Sum*=2
                Sum+=(gray[h-1,w+1] > gray[h,w])
            ## h,w+1
            if w==W-1:
                Sum*=2
            else:
                Sum*=2###
                Sum+=(gray[h,w+1] > gray[h,w])
            ## h+1,w+1
            if h==H-1 or w==W-1:
                Sum*=2
            else:
                Sum*=2###
                Sum+=(gray[h+1,w+1] > gray[h,w])
            ## h+1,w
            if h==H-1:
                Sum*=2
            else:
                Sum*=2###
                Sum+=(gray[h+1,w] > gray[h,w])
            ## h+1,w-1
            if h==H-1 or w==0:
                Sum*=2
            else:
                Sum*=2###
                Sum+=(gray[h+1,w-1] > gray[h,w])
            ## h,w-1
            if w==0:
                Sum*=2
            else:
                Sum*=2###
                Sum+=(gray[h,w-1] > gray[h,w])
            img_feature[h,w]=Sum
    # return (sum(img_feature.reshape(-1)>4)/(H*W*1.0))
    return(img_feature)
def get_shape(imgPath):
    return(cv2.cvtColor(np.array(Image.open(imgPath)), cv2.COLOR_BGR2GRAY).shape)
def gray2array_ave(grayImg):
    height, width = grayImg.shape
    pixCount=0
    pixSum=0
    pixList=[]
    for line in range(height):
        for pixel in range(width):
            pixCount+=1
            pixSum+=grayImg[line][pixel]
    pixAve = pixSum /pixCount
    for line in range(height):
        for pixel in range(width):
            pixList.append(grayImg[line][pixel]-pixAve)
    return np.array(pixList)
def gray2array_raw(grayImg):
    height, width = grayImg.shape
    pixList=[]
    for line in range(height):
        for pixel in range(width):
            pixList.append(grayImg[line][pixel])
    return np.array(pixList)
def rgb2gray(rgb):
    gray=cv2.cvtColor(np.array(rgb), cv2.COLOR_BGR2GRAY)
    return gray
def show_img(img,pos=[100,100]):
    cv2.imshow("img",img)
    cv2.moveWindow("img",pos[0],pos[1])
    cv2.waitKey(0)
def info():
    print("compare_LBP_featrue(basePath, checkPath, roi) -> float")
    print("compare_cos_featrue(basePath, checkPath, roi) -> float")
    print("cos(baseArray,checkArray) -> float")
    print("cut_roi(jpgPath,roi=(xmin,ymin,xmax,ymax))) -> Image")
    print("get_LBP_featrue(roi) -> grayImg")
    print("gray2array_ave(grayImg) -> numpy.array")
    print("gray2array_raw(grayImg) -> numpy.array")
    print("rgb2gray(rgb) -> grayImg")
    print("show_img(img,pos=[100,100]) -> void")
    exit()
