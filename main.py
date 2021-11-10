from __future__ import print_function

import json
import os
import sys

if sys.version_info[0] >= 3:
    from urllib.request import urlretrieve
else:
    # Not Python 3 - today, it is most likely to be Python 2
    # But note that this might need an update when Python 4
    # might be around one day
    from urllib import urlretrieve


def download(url, fileName, savePath='./'):
    def reporthook(block_num, block_size, total_size):
        read_so_far = block_num * block_size
        if total_size > 0:
            percent = read_so_far * 1e2 / total_size
            s = "\r%5.1f%% %*d / %d" % (
                percent, len(str(total_size)), read_so_far, total_size)
            print(s, end=' ')
        else:
            print("\r%d / unknown" % (read_so_far), end=' ')
        sys.stdout.flush()

    filePath = os.path.join(savePath, fileName)
    print("\rsave path:%s" % filePath)

    if not os.path.exists(savePath):
        print("make dir:%s" % savePath)
        os.makedirs(savePath)

    if not os.path.isfile(filePath):
        print("downloading data from: %s" % url)
        urlretrieve(url, filePath, reporthook=reporthook)
        print("\ndownload finished!")
    else:
        print("file already exsits!")

    fileSize = os.path.getsize(filePath)
    print("file size = %.2f MB" % (fileSize/1024/1024))


if __name__ == '__main__':

    downloadCounter = 0

    # 在手机端获取 PUB 社群的网页链接，粘贴到 PC 浏览器上，之后扫码登陆，即可看到相关的接口
    file = "list.json"

    with open(file, "r") as f:
        data = json.load(f)
        for res in data.get("data"):
            subject = res.get("title")
            speech = res.get("file_json")

            for item in speech:
                url = item.get("url")
                fileName = item.get("name")
                print("begin download: %s" % fileName)
                download(url, fileName, os.path.join("./", subject))
                downloadCounter += 1

    print("file count %s" % downloadCounter)
