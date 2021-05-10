#encoding=utf-8
import os
import shutil
def copy_files_refer_dir(srcDir,srcForm,ReferDir,tarDir):
    allRefers=get_sorted_files(ReferDir)
    for refer in allRefers:
        file=refer.split('.')[0]+srcForm
        srcPath=os.path.join(srcDir,file)
        tarPath=os.path.join(tarDir,file)
        try:
            shutil.copy(srcPath,tarPath)
        except:
            pass
def list_all_files(rootdir):
    _files = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
           path = os.path.join(rootdir,list[i])
           if os.path.isdir(path):
              _files.extend(list_all_files(path))
           if os.path.isfile(path):
              _files.append(list[i])
    return _files
def list_all_filePaths(rootdir):
    _files = []
    list = os.listdir(rootdir) #列出文件夹下所有的目录与文件
    for i in range(0,len(list)):
           path = os.path.join(rootdir,list[i])
           if os.path.isdir(path):
              _files.extend(list_all_filePaths(path))
           if os.path.isfile(path):
              _files.append(path)
    return _files
def get_sub_dirs(rootDir):
    for root,dirs,files in os.walk(rootDir):
        if root==rootDir:
            return dirs
    return []
def get_files(rootDir):
    #获取目录第一层所有文件
    for root,dirs,files in os.walk(rootDir):
        if root==rootDir:
            return files
    return []
def get_sorted_files(fileDIr):
    for root,dirs,files in os.walk(fileDIr):
        if root==fileDIr:
            return sorted(files)
    return []
def mkdir(fileDIr):
    if not os.path.exists(fileDIr):
        os.mkdir(fileDIr)
        # print("Creat fileDIr ",fileDIr)
def rm_mkdir(fileDIr):
    if not os.path.exists(fileDIr):
        os.mkdir(fileDIr)
        print("Creat fileDIr {}".format(fileDIr))
    else:
        cmd=input('Remove {}\nCheck again before enter n/y?\n'.format(fileDIr))
        if cmd =='y' or cmd=='Y':
            try:
                shutil.rmtree(fileDIr)
            except:
                os.rmdir(fileDIr)
            os.mkdir(fileDIr)
            print("Remove & Creat fileDIr {}".format(fileDIr))
        else:
            print('Gave up')
            exit()
def shutil_by_refer(referDir,referForm,opForm,srcDir,tarDir):
    allRefers=[x for x in get_files(referDir) if referForm in x]#审核为.refer形成列表
    for refer in allRefers:
        sour=refer.split('.')[0]+opForm
        tar=refer.split('.')[0]+opForm
        srcPath=os.path.join(srcDir,sour)
        tarPath=os.path.join(tarDir,tar)
        shutil.copy(srcPath,tarPath)
def info():
    print("get_sub_dirs(rootDir) -> class list")
    print("get_files(fileDIr) -> class list")
    print("get_sorted_files(fileDIr) -> class list")
    print("mkdir(fileDIr) -> void")
    exit()