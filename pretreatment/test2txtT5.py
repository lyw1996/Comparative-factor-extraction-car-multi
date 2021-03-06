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
def write_data(filewrite,raw_sentence,list_stan):
	f3=open(filewrite,'w')
	list_result = []
	for i in range(len(raw_sentence)):
		list_fea = nlp.pos_tag(raw_sentence[i].sentence)  # 存储的是tuple
		# print(list_fea)
		list_parse = nlp.parse(raw_sentence[i].sentence)  # 存储的是树
		# print(list_parse)
		list_parse_fea = (list_parse.split('\r\n'))
		# print(list_parse.split('('))
		for i2 in range(1, len(list_parse_fea)):
			list_parse_fea[i2] = list_parse_fea[i2].strip()
		# print(list_parse_fea[i])
		num = 0
		list_chunk = []
		for i3 in range(len(list_parse_fea)):
			for j3 in range(num, len(list_fea)):
				if list_fea[j3][1] + ' ' + list_fea[j3][0] in list_parse_fea[i3]:
					if 'DNP' in list_parse_fea[i3]:
						num = num + 1
						list_chunk.append('DNP')
					# print('DNP')
					elif 'ADVP' in list_parse_fea[i3]:
						num = num + 1
						list_chunk.append('ADVP')
					# print('ADVP')
					elif 'ADJP' in list_parse_fea[i3]:
						num = num + 1
						list_chunk.append('ADJP')
					# print('ADJP')
					elif 'PP' in list_parse_fea[i3]:
						num = num + 1
						list_chunk.append('PP')
					# print('PP')
					elif 'VP' in list_parse_fea[i3]:
						num = num + 1
						list_chunk.append('VP')
					# print('VP')
					elif 'NP' in list_parse_fea[i3]:
						num = num + 1
						list_chunk.append('NP')
					# print('NP')
					elif 'QP' in list_parse_fea[i3]:
						num = num + 1
						list_chunk.append('QP')
					# print('QP')
					elif 'LCP' in list_parse_fea[i3]:
						num = num + 1
						list_chunk.append('LCP')
					elif 'IP' in list_parse_fea[i3]:
						num = num + 1
						list_chunk.append('IP')
					elif 'INC' in list_parse_fea[i3]:
						num = num + 1
						list_chunk.append('INC')
					# print('LCP')
					else:
						count = 0
						for a in range(i3 - 1, 0, -1):
							# print(list_parse_fea[a])
							sl = list_parse_fea[a].count('(')
							# print(sl)
							sr = list_parse_fea[a].count(')')
							count = count + sl - sr
							if count > 0:
								result_0 = list_parse_fea[a].split('(')
								result_1 = result_0[1]

								num = num + 1
								list_chunk.append(result_1)
								# print(result_1)
								break
							else:
								count = count
				else:
					break
		'''
		if len(list_chunk) != len(list_fea):
			print(raw_sentence[i].index)
			print(nlp.parse(raw_sentence[i].sentence))
			print(len(list_chunk), len(list_fea))
	'''
		for n in range(len(list_fea)):
			result = Defi_class.Feature(raw_sentence[i].index, list_fea[n][0], list_fea[n][1], '', '', '', 'OTHERS')
			result.chunk = list_chunk[n]
			list_result.append(result)


	print(list_result.__len__())
	print(list_stan.__len__())
	for j1 in range(len(list_result)):
		f3.write(list_result[j1].word + ' ' + list_result[j1].pos+ ' ' + list_result[j1].chunk)
		f3.write('\n')

	return write_data


write_data('..\CRF++\\testT5.txt',raw_sentence,list_stan)
