#!/usr/bin/python
# -*- coding :utf-8 -*-
import Defi_class
import Defi_func
import re
import numpy as np
from stanfordcorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP(r'E:\stanford\stanford-corenlp-full-2018-02-27/', lang='zh')

kw_candidate=Defi_func.readkeywords()
#从语料库中提取比较句
#list_sentence存放比较句的编号，没有任何标签的纯比较句
def sentence_data(fileresult):
	f1=open(fileresult,'r')
	list_sentence=[]
	for line1 in f1.readlines():
		if line1=='\n':
			break
		else:
			result_0 = line1.split('\t')  # 横向制表符对字符串进行切片
			result_1 = result_0[1].split('<')
			result_2 = result_1[0]  # 存放的是没有任何标签的整个句子
			raw_sentence=Defi_class.raw_sentence(result_0[0],result_2)
			list_sentence.append(raw_sentence)
			#print(result_2) 测试成功
	#print(list_sentence.__len__())  测试成功
	list_sentence=np.array(list_sentence)
	return list_sentence

#读取手工标注的答案
#存入类为sentence的列表中
def result_data(fileanswer):
	f1=open(fileanswer,'r')
	list_stan = []
	for line1 in f1.readlines():
		if line1 == '\n':
			break
		else:
			result_0 = line1.split()
			#print(len(result_0))
			senten = Defi_class.Standard(result_0[1], result_0[3], result_0[4], result_0[5], result_0[6],result_0[7])
			list_stan.append(senten)
	list_stan=np.array(list_stan)
	return list_stan


raw_sentence=sentence_data('..\data\多重比较汽车训练比较句.txt')
list_stan=result_data('..\data\多重比较汽车训练任务2.2改进.txt')
def write_data(filewrite,raw_sentence,list_stan,kw_candidate):
	f3=open(filewrite,'w')
	list_result = []
	for i in range(len(raw_sentence)):
		list_fea = nlp.pos_tag(raw_sentence[i].sentence)  # 存储的是tuple
		print(list_fea)
		for num in range(len(list_fea)):
			result = Defi_class.Feature(raw_sentence[i].index, list_fea[num][0], list_fea[num][1],'','NO','','OTHERS')
			# f3.write(result.index +' '+result.word+' '+result.pos)
			# f3.write('\n')
			list_result.append(result)
	print(list_result.__len__())
	print(list_stan.__len__())
	for j1 in range(len(list_result)):
		for j3 in range(len(kw_candidate)):
			if list_result[j1].word in kw_candidate[j3]:
				list_result[j1].keyword='YES'
				break

		f3.write(list_result[j1].word + ' ' + list_result[j1].pos+ ' ' + list_result[j1].keyword)
		f3.write('\n')
	print(len(list_result))
	return write_data


write_data('..\CRF++\\testT2.txt',raw_sentence,list_stan,kw_candidate)
