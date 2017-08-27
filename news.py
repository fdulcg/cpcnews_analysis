#coding:utf-8
import logging
from pymongo import MongoClient
import codecs
import random
import json
from snownlp import SnowNLP
from stanfordcorenlp import StanfordCoreNLP
def createLogger():

    logger_name = "crawl"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    # create file handler
    log_path = "error.log"
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.WARN)

    # create formatter
    fmt = "%(asctime)-15s %(levelname)s %(filename)s %(lineno)d %(process)d %(message)s"
    datefmt = "%a %d %b %Y %H:%M:%S"
    formatter = logging.Formatter(fmt, datefmt)

    # add handler and formatter to logger
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

def writejson(result,filename):
    with open('./cosejs/'+filename+'.json','w',encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

def sentokenize(sent):
    retlist = []
    ret = []
    for s_str in sent.split('。'):
        if '？' in s_str:
            retlist.extend(s_str.split('？'))
        elif '！' in s_str:
            retlist.extend(s_str.split('！'))
        elif '；' in s_str:
            retlist.extend(s_str.split('；'))
        else:
            retlist.append(s_str)
    for each in retlist:
        if each != '':
            ret.append(each)
    return ret


def sentsingle(sent):
    ret = []
    for s_str in sent.split('，'):
        if s_str != '':
            ret.append(s_str)
    return  ret



def getyinhao(sentence):
    if '“' in sentence and '”' in sentence:
        idstring = ''
        begin = False
        for each in sentence:
            if begin:
                if each == '”':
                    begin = False
                    if idstring not in keyword.keys():
                        print(idstring)
                else:
                    idstring += each
            if each == '“':
                begin = True

if __name__ == "__main__":
    logger = createLogger()
    client = MongoClient('mongodb://mongo url/')
    db_auth = client.admin
    db_auth.authenticate('username', 'password')
    keyword = {word.strip('\n').strip(): 0 for word in codecs.open('dict.txt','r','utf-8').readlines()}
    db = client.XXX
    dictlist = {}

    edgedict = {}
    hasegdelist = []
    for news in db.find({'content': {'$exists': True}}):
        content = news.get('content').strip('\n').strip('\t')
        sentences = sentokenize(content)
        for sentence in sentences:
            singlesent = sentsingle(sentence)
            for single in singlesent:
                baselist = []
                for word in keyword.keys():
                    if word in single and word!='':
                        baselist.append(word)
                        keyword[word] += 1
                if len(baselist)>1:
                    if len(baselist)>2:
                        retlist = []
                        templist = baselist
                        for each in baselist:
                            for one in templist:
                                if each != one:
                                    if [each,one] not in retlist and [one,each] not in retlist:
                                        retlist.append([each,one])
                        for thelist in retlist:
                            if thelist[0] not in hasegdelist:hasegdelist.append(thelist[0])
                            if thelist[1] not in hasegdelist: hasegdelist.append(thelist[1])
                            if thelist[0] in edgedict.keys():
                                if thelist[1] in edgedict[thelist[0]].keys():
                                    edgedict[thelist[0]][thelist[1]] += 1
                                else:
                                    edgedict[thelist[0]][thelist[1]] = 1
                            else:
                                edgedict[thelist[0]] = {thelist[1]:1}


        # for each in nlp.ner(content):
        #     if each[1]!='O' and each[1]!='NUMBER' and len(each[0])>1:
        #         if each[0] not in dictlist.keys():
        #             print(each[0]+':'+each[1])
        #             dictlist[each[0]] = 1
        #         else:
        #             dictlist[each[0]] += 1

    newkeyword = {}
    for it in keyword.keys():
        if it in hasegdelist:
            newkeyword[it] = keyword[it]
    sort = sorted(newkeyword.items(), key=lambda e: e[1], reverse=True)

    # edgesort = sorted(edgedict.items(), key=lambda e: e[1], reverse=True)
    print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
    nodeNum = len(hasegdelist)
    print(str(sort))
    print(str(edgedict))
    sum = 0
    for score in newkeyword.values():
        sum+=score
    nodescore = {}
    nodeid = {}
    nodexy = {}

    xyset = []
    for i in range(2*nodeNum+2):
        xyset.append(random.uniform(150, 1000))
    beginNum = 1000
    for eac in newkeyword.keys():
        scores = newkeyword[eac] / sum
        nodescore[eac] = scores
        if newkeyword[eac]!=0:
            beginNum += 1
            nodeid[eac] = beginNum
        nodexy[eac] = [xyset.pop(),xyset.pop()]

    print(str(nodescore))
    print(str(nodeid))
    print(str(nodexy))
    # print(str(listsort))
        # s = SnowNLP(content)
        # for keyword in s.keywords(5):
        #     print(keyword)
        # for summery in s.summary(3):
        #     print(summery)
        # for ent in nlp.ner(content):
        #     print(str(ent[0])+':'+str(ent[1]))
    edgecolorlist = ["spd","coloc","coexp","pi","path","predict"]


    datalist = []
    for name in newkeyword.keys():
        idInt = nodeid[name]
        id = str(idInt)
        score = nodescore[name]
        x = nodexy[name][0]
        y = nodexy[name][1]
        ret = {
            "data":{
                    "id": id,
                    "idInt": idInt,
                    "name": name,
                    "score": score,
                    "query": True,
                    "gene": True
            },
            "position": {
                "x": x,
                "y": y
            },
            "group": "nodes",
            "removed": False,
            "selected": False,
            "selectable": True,
            "locked": False,
            "grabbed": False,
            "grabbable": True,
            "classes": ""
        }
        datalist.append(ret)

    startNum = 10000
    for source1 in edgedict.keys():
        for target1 in edgedict[source1].keys():
            times = edgedict[source1][target1]
            for i in range(times):
                source = nodeid[source1]
                target = nodeid[target1]
                weight = 0.013092303
                group = random.sample(edgecolorlist, 1)[0]
                intn = True
                startNum += 1
                rIntnId = startNum
                mid = 'e' + str(rIntnId)
                edict = {
                    "data": {
                        "source": source,
                        "target": target,
                        "weight": weight,
                        "group": group,
                        "networkId": 1215,
                        "networkGroupId": 19,
                        "intn": True,
                        "rIntnId": rIntnId,
                        "id": mid
                    },
                    "position": {},
                    "group": "edges",
                    "removed": False,
                    "selected": False,
                    "selectable": True,
                    "locked": False,
                    "grabbed": False,
                    "grabbable": True,
                    "classes": ""
                }
                datalist.append(edict)

    writejson(datalist,'data3')







