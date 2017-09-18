#!/usr/bin/python3
import requests
import hashlib
import random
import re
import json


# 百度翻译API接口
appId = '20170915000082913'
secretKey = 'MVuquLxuANruv_rghf1f'
url = 'http://api.fanyi.baidu.com/api/trans/vip/translate'
contantDict = {}


def mulLangTranslate(query, fromlang, tolang):
    """
    多语言翻译，将字符串从源语言翻译为目标语言
    :param query: 需要翻译的字符串
    :param fromlang: 源语言类型
    :param tolang: 目标语言类型
    :return: contantDict 以字典的形式返回翻译结果
    """
    global contantDict
    salt = random.randint(32768, 65535)
    sign = appId + query + str(salt) + secretKey
    m = hashlib.md5(sign.encode("utf-8"))
    sign = m.hexdigest()
    theUrl = url + '?q=' + query + '&from=' + fromlang + '&to=' + tolang \
        + '&appid=' + appId + '&salt=' + str(salt) + '&sign=' + sign
    try:
        r = requests.get(url=theUrl)
        contantDict = json.loads(r.text)

    except Exception as msg:
        print(msg)
    return contantDict


# 文件内容处理
def fileStrHandle(content, pattern):
    """
    文本文件格式处理，将形如"key:value"或"key=value"，并以换行符'\n'结尾的字符串，使用正则
    表达式筛选出来，并返回[keys],[values]的列表
    :param content: 形如"key:value"或"key=value"的文件内容
    :param pattern: 文件格式标志，以确定以何种正则表达式筛选
    :return: 返回[keys],[values]的列表
    """
    if pattern == '1':  # 匹配形如"key:value"
        keypat = r'[a-zA-Z_][a-zA-Z0-9_]*:'
        valuepat = r':.+'
    elif pattern == '2':  # 匹配形如"key=value"
        keypat = r'.*='
        valuepat = r'=.+'
    matchkeys = re.findall(keypat, content)
    matchvalues = re.findall(valuepat, content)
    print(len(matchkeys))
    print(len(matchvalues))
    for i in range(0, len(matchvalues)):
        if pattern == '1':
            matchvalues[i] = matchvalues[i].replace(':', '')+'\n'
        elif pattern == '2':
            matchvalues[i] = matchvalues[i].replace('=', '')+'\n'
    return matchkeys, matchvalues


# 语言翻译提示
def showTips():
    """
    提示支持的翻译语种
    :return: none
    """
    tips = {'auto': '自动检测', 'zh': '中文', 'en': '英文', 'yue': '粤语', 'jp': '日语', 'kor': '韩语',
            'fra': '法语', 'spa': '西班牙语', 'th': '泰语', 'ara': '阿拉伯语', 'ru': '俄语', 'pt': '葡萄牙语',
            'de': '德语', 'it': '意大利语', 'el': '希腊语', 'nl': '荷兰语', 'pl': '波兰语', 'bul': '保加利亚语',
            'est': '爱莎尼亚语', 'dan': '丹麦语', 'fin': '芬兰语', 'cs': '捷克语', 'rom': '罗马利亚语', 'slo': '斯洛文尼亚语',
            'swe': '瑞典语', 'hu': '匈牙利语', 'cht': '繁体中文', 'vie': '越南语'}
    for key, value in tips.items():
        print(str(key)+"---"+str(value)+"\n")


# 文件读取
class FileIO:
    """Summary of class here
    该类用于文件读写，不修改源文件，直接将翻译结果以追加形式写入目标文件
    Args:
        inputfilename: 输入文件名
        content: 需要翻译的文本
        keys(list):保存key
        query: 经正则表达式筛选之后的字符串
        fromLang: 源语言类型
        toLang: 目标语言类型
        patter: 文件格式
    """
    inputfilename = ''
    content = ''
    partvalues = []
    keys = []
    values = []
    query = ''
    fromLang = ''
    toLang = ''
    pattern = ''
    lines = 0

    def __init__(self, infile, fromlang, tolang, ft):
        self.inputfilename = infile
        self.fromLang = fromlang
        self.toLang = tolang
        self.pattern = ft

    def fileRead(self):
        with open(self.inputfilename, mode='r', encoding='utf-8') as f:
            self.content = f.read()
        (self.keys, self.partvalues) = fileStrHandle(self.content, self.pattern)

    def fileWrite(self):
        reslist = []
        for i in range(1, len(self.partvalues)):
            if i % 100 != 0:                              # 一次读取100行
                self.query += self.partvalues[i-1]
            else:
                self.query += self.partvalues[i-1]
                results = mulLangTranslate(self.query, self.fromLang, self.toLang)
                if 'trans_result' in results:
                    reslist = results['trans_result']
                    self.values += reslist
                    self.query = ''
        self.query += self.partvalues[i]
        results = mulLangTranslate(self.query, self.fromLang, self.toLang)
        if 'trans_result' in results:
            reslist = results['trans_result']
            self.values += reslist
        print(len(self.values))
        print(len(self.keys))

        with open(str(self.toLang)+".js", mode='a+', encoding='utf-8') as f:
            for j in range(0, len(self.keys)):
                print(j)
                f.writelines(self.keys[j]+self.values[j]['dst']+'\n')


if __name__ == '__main__':
    filename = input("请输入文件名:")
    showTips()
    filetype = input("请输入文件格式:\n1) a:b 2) a=b\n")
    srclang = input("请输入源语言:(若不确定，请输入auto)\n")
    dislang = input("请输入目标语言:(必须指定，不能输入auto)\n")
    x = FileIO(filename, srclang, dislang, filetype)
    x.fileRead()
    x.fileWrite()



