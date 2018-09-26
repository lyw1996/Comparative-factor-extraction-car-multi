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
	num_position=0
	for i in range(len(raw_sentence)):
		num_position=num_position+1
		list_fea = nlp.pos_tag(raw_sentence[i].sentence)  # 存储的是tuple
		#print(list_fea)
		for num in range(len(list_fea)):
			if list_fea[num][1]=='PU':
				result = Defi_class.Feature(num_position, list_fea[num][0], list_fea[num][1], '', 'NO', 'false',
											'OTHERS')
				num_position=num_position+1
			else:
				result = Defi_class.Feature(num_position, list_fea[num][0], list_fea[num][1], '', 'NO', 'LBF',
											'OTHERS')
			list_result.append(result)
	#print(list_result.__len__())
	#print(list_stan.__len__())

	list_result[- 1].index=1
	for j1 in range(len(list_result)):
		if list_result[j1].index < list_result[j1 - 1].index:
			print(j1 - 1)
			list_result[j1].position = 'LAF'
			list_result[j1].index = list_result[j1].index+1
			#print(list_result[j1].index)
		for j3 in range(len(kw_candidate)):
			if list_result[j1].word in kw_candidate[j3]:
				list_result[j1].keyword='YES'
				list_result[j1].position = 'KW'
				list_result[j1].index=list_result[j1].index+1
				break
		if list_result[j1].pos=='PU':
			list_result[j1].position = 'none'

		f3.write(list_result[j1].word + ' ' + list_result[j1].keyword+ ' ' + list_result[j1].position)
		f3.write('\n')
	print(list_result.__len__())
	return write_data



write_data('..\CRF++\\testT3.txt',raw_sentence,list_stan,kw_candidate)
