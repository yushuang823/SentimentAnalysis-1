# !/usr/bin/env python
# -*- coding: utf-8 -*-
from matplotlib import image
from wordcloud import WordCloud
import jieba
import PIL
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import matplotlib
from pylab import mpl
import re

mpl.rcParams['font.sans-serif'] = ['SentyTang']     # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False
matplotlib.rc('xtick', labelsize=14)
matplotlib.rc('ytick', labelsize=14)

def preprocessor(text):
    # 删除所有的HTML标记
    text = re.sub('<[^>]*>', '', text)
    # 去除数字
    # text = re.sub('\d', '', text)
    # 英文字母
    text = re.sub('[a-z0-9]', '', text)
    # text = re.sub
    # 寻找表情符号
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text)
    # 删除标点符号，将表情符号添加到评论的最后
    text = re.sub('[\W]+', ' ', text.lower()) + ''.join(emoticons).replace('-', '')
    return text

path = r'D:\Users\work\PycharmProjects\SentimentAnalysis-JD\SentimentAnalysis\StopwordsCN.txt'

def getStopWords(stopWordsName):
    with open(stopWordsName, encoding='utf-8') as f:
         stopWords = [word.replace("\n", "") for word in f.readlines()]
    return stopWords

stopword_list = getStopWords(path)

def tokenize_text(text):
        seg_list = jieba.cut(text, cut_all=False)
        tokens = (' '.join(seg_list))
        # tokens = jieba.cut(text)
        # # tokens = [token.strip() for token in tokens]
        # tokens = [''.join(token) for token in tokens]
        return tokens

def remove_stopwords(text):
        tokens = tokenize_text(text)
        filtered_tokens = [token for token in tokens if token not in stopword_list]
        filtered_text = ''.join(filtered_tokens)
        return filtered_text

def wordcloudplot(txt):
    path=r'C:\Windows\Fonts\simkai.ttf'
    # path= np.unicode(path, 'utf8').encode('gb18030')
    alice_mask = np.array(PIL.Image.open(r'C:\Users\work\Desktop\ma.png'))
    wordcloud = WordCloud(font_path=path,
                          background_color="white",
                          margin=5, width=1800, height=800,mask=alice_mask,max_words=2000,max_font_size=60,
                          random_state=42)
    wordcloud = wordcloud.generate(txt)
    wordcloud.to_file('输出文件')
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()

def main():
    a=[]
    b = []
    new_line = ''
    with open(r'E:\wendang\shujuji\ec_jd_goods_comment.json', 'r', encoding='utf-8') as sentence:
        for line in sentence:
            new_line = preprocessor(line)
            new_line = remove_stopwords(new_line)
            new_line = re.sub('\s+', ' ', new_line)
            b.append(new_line)
    # f=open(r'C:\Users\work\Desktop\pinglun.txt','r',encoding='utf-8').read()
    # words=list(jieba.cut(f))
    tongji = Counter(b).most_common(20)

    d = {key: value for (key, value) in tongji}

    # for i in list(d.keys()):
    #     if i in b:
    #         d.pop(i)
    # print (d)
    label = list(d.keys())
    y = list(d.values())
    idx = np.arange(len(y))
    plt.barh(idx,y)
    plt.yticks(idx+0.4,label)
    plt.xlabel('出现次数',fontsize = 20,labelpad = 5)
    plt.ylabel('关键词',fontsize= 20,labelpad = 5)
    plt.title('出现最高词频数可视化图',fontsize= 25)
    plt.savefig('输出词频图标')
    plt.show()
    # 绘制pie chart on polar axis
    N = len(d)
    theta = np.arange(0.0, 2*np.pi,2*np.pi/N)
    radii = y
    width = np.pi/6
    ax = plt.subplot(111,projection='polar')
    bars = ax.bar(theta, radii, width = width, bottom = 0.0)
    plt.xticks(theta+np.pi/12,label)

    for r, bar in zip(radii, bars):
        bar.set_facecolor(plt.cm.viridis(r / 10.))
        bar.set_alpha(0.5)

    plt.savefig('输出pie极坐标图')
    plt.show()

    for word in d:
        if len(word)>1:
            a.append(word)
    txt=r' '.join(a)
    wordcloudplot(txt)   #输出词云

if __name__=='__main__':
    main()

