import urllib.request
import requests
import os
from bs4 import BeautifulSoup

# 替换成自己的文件夹
dirString = "/Users/lina/Desktop/music/"
# 替换成自己想下载的歌单
playListString = "http://music.163.com/playlist?id=2221867611&userid=99341654/"

def startDownload(values):
    print ('歌曲数目')
    print (len(values))
    downNum=0
    for x in values:
        if not os.path.exists(dirString + x['name'] + '.mp3'):
            print('当前任务*********' + x['name'] + '.mp3 *****')
            url = 'http://music.163.com/song/media/outer/url?id=' + x['id'] + '.mp3'
            try:
                urllib.request.urlretrieve(url,dirString + x['name'].replace('/','') + '.mp3')
                downNum = downNum + 1
            except:
                x=x-1
    print('Download complete ' + str(downNum) + ' files !')
    pass

def getMusicData(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    headers={'User-Agent':user_agent}
    webData=requests.get(url,headers=headers).text
    soup=BeautifulSoup(webData,'lxml')
    find_list=soup.select('a')
    tempArr = []
    for music in find_list:
        if music.has_attr("href"):
            if str(music.attrs["href"]).startswith("/song?id="):
                id=str(music.attrs["href"]).replace("/song?id=", "")
                try:
                    tempArr.append({
                        "id": id,
                        "url": "http://music.163.com/song/media/outer/url?id=" + id + ".mp3",
                        "name": music.text
                    })
                except:
                    print('无法下载的歌曲：'+music)
                    pass
    return tempArr
    
if __name__ == '__main__':
    if not os.path.exists(dirString):
        os.mkdir(dirString)
    musicData = getMusicData(playListString)
    print(startDownload(musicData))