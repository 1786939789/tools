import os
def avi2mp4(aviPath,mp4Path):
    command='ffmpeg -i '+aviPath+' -y -c:v libx264 -b:v 1200k '+mp4Path
    print(command)
    try:
    	os.system(command)
    except:
    	error()
def dav2mp4(davPath,mp4Path):
    command='ffmpeg -i "' + davPath + '"  "' + mp4Path + '"\n'
    print(command)
    try:
    	os.system(command)
    except:
    	error()
def info():
    print("avi2mp4(aviPath,mp4Path) -> void")
    print("dav2mp4(davPath,mp4Path) -> void")
    exit()
def error():
    print("Command failed")
