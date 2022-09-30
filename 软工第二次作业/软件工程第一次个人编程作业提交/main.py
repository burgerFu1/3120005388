import re
import jieba
import gensim
import os
import sys


def analyze(analyze1, analyze2):
    # 调用gensim模块计算cos近似
    texts = [analyze1, analyze2]
    dictionary = gensim.corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features=len(dictionary))
    cos = dictionary.doc2bow(analyze1)
    cosine_sim = similarity[cos][1]
    return cosine_sim


def getContents(path):
    string = ''
    # 按行读取文件内容
    with open(path, 'r', encoding='UTF-8') as f:
        line = f.readline()
        while line:
            string = string + line
            line = f.readline()
    return string


def filter(target):
    # 过滤除正文以外内容
    pattern = re.compile(u"[^a-zA-Z0-9\u4e00-\u9fa5]")
    target = pattern.sub("", target)
    # 调用jieba模块分成词汇
    result = jieba.lcut(target)
    print("[*] 进行词义分析: ")
    print(result)
    return result


def main(path1, path2, res):
    print("论文文件的绝对路径: " + path1)
    print("论文文件的绝对路径: " + path2)
    print("保存结果的路径: " + res)

    # 先对路径文件进行判断是否存在。若存在则进入下一步，否则则提示不存在且退出程序
    if not os.path.exists(path1):
        print("[-] 论文文件不存在")
        exit(0)
    if not os.path.exists(path2):
        print("[-] 抄袭版论文文件不存在！")
        exit(0)

    # 读取文件输出
    content1 = getContents(path1)
    print("[*] 论文文件内容: ")
    print(content1)

    content2 = getContents(path2)
    print("[*] 可能抄袭论文文件内容: ")
    print(content2)

    # 过滤文件内容除正文以外的内容
    contentAfterFilter1 = filter(content1)
    contentAfterFilter2 = filter(content2)

    # 进行词义分析
    similarity = analyze(contentAfterFilter1, contentAfterFilter2)

    # 进行精度过滤
    result = round(similarity.item(), 2)
    flush = "[+] 近似度为: " + str(result)
    # 保存结果并输出
    with open(res, 'w') as f:
        f.write(flush)
    print(flush)


if __name__ == '__main__':
    # 首先判断用户输入参数个数是否正确，正确则传入main函数
    if len(sys.argv) < 4:
        print("[-] 请检查参数是否正确")
        print("python3 main.py 论文文件的绝对路径 论文文件的绝对路径 保存结果的路径")
        exit(0)

    main(sys.argv[1], sys.argv[2], sys.argv[3])



