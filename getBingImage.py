#coding:utf-8
import urllib
import re
import os
import os.path
import sys
import random

PATH = '~/Library/bingImages'
url = 'http://www.bing.com/'
imgRE = r'g_img={url: "(.*?)"'
configFloder = '~/Library/bingImages/config'



def resolvePath(path):
    path = os.path.expanduser(path)  # to transform relative path to absolute path
    if os.path.isdir(path) == False:
        print('dir didn\'t exist, created it.')
        os.mkdir(path)
    return path
PATH = resolvePath(PATH)
configFloder = os.path.expanduser(configFloder)
logFilePath = os.path.join(configFloder, 'log.txt')


def log(message):
    resolvePath(configFloder)
    with open(logFilePath, 'w') as f:
        f.write(message)

def getDirectoryImageList(path):
    fileList = os.listdir(path)
    returnfilelist = []
    for singleFile in fileList:
        extname = os.path.splitext(singleFile)[1]
        if extname != '':
            returnfilelist.append(singleFile)
    return returnfilelist

def getLog():
    with open(logFilePath, 'r') as f:
        return f.read().decode('utf-8')

def getBingImage():
    f = urllib.urlopen(url)
    content = f.read().decode('utf-8')

    match = re.search(imgRE, content)
    if match:
        # print(match.group(1))
        imgUrl = url + match.group(1)
    else:
        print('failed')
    # 保存图片
    imageName = os.path.split(imgUrl)[1]
    imgPath = os.path.join(PATH, imageName)
    with open(imgPath, 'wb') as f:
        data = urllib.urlopen(imgUrl)
        data = data.read()
        f.write(data)
    log(imgPath)
    return imgPath
def randomChoose():
    wallpapers = getDirectoryImageList(PATH)
    if len(wallpapers) == 0:
        return
    seed = random.randint(0, len(wallpapers)-1)
    return os.path.join(PATH, wallpapers[seed])

def clean():
    wallpapers = getDirectoryImageList(PATH)
    for index in wallpapers:
        os.remove(os.path.join(PATH,index))

def garbage():
    garbageImage = getLog()
    os.remove(garbageImage)
    randomChoose()

def output(func):
    sys.stdout.write(func())


if __name__ == '__main__':
    # getBingImage()
    output(randomChoose)
if __name__ != '__main__':
    query = ''
    if (len(sys.argv) == 2):
        query = sys.argv[1]
    else:
        raise Exception('please give your argvs')
    if query == 'list':
        pass
    elif query == 'random':
        output(randomChoose)
        getBingImage()
    elif query == 'clean':
        clean()
    elif query == 'garbage':
        garbage()
    elif query == 'now':
        output(getBingImage)
    else:
        raise Exception('please provide a argv!')

