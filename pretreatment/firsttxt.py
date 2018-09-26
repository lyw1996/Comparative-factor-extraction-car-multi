#!/usr/bin/python
# -*- coding :utf-8 -*-


import Defi_class


f1=open('..\\data\汽车测试任务2.2改进.txt','r')
f2=open('..\\data\多重比较汽车测试任务2.2改进.txt','w')
f3=open('..\\data\汽车训练任务2.2改进.txt','r')
f4=open('..\\data\多重比较汽车训练任务2.2改进.txt','w')
f5=open('..\data\汽车测试比较句.txt','r')
f6=open('..\data\多重比较汽车测试比较句.txt','w')
f7=open('..\data\汽车训练比较句.txt','r')
f8=open('..\data\多重比较汽车训练比较句.txt','w')

#测试模块
list=[]
list_index_test=[]
for line1 in f1.readlines():
	if line1 == '\n':
		break
	else:
		result1=line1.split()
		list.append(result1[0])
		if '|' in line1:
			list_index_test.append(result1[0])
for i in range(1,len(list)):
	if list[i]==list[i-1]:
		list_index_test.append(list[i])
list_index=sorted(set(list_index_test))
print(len(list_index))
f1=open('..\\data\汽车测试任务2.2改进.txt','r')
for line1 in f1.readlines():
	if line1 == '\n':
		break
	else:
		result_0 = line1.split()
		for i in range(len(list_index)):
			if result_0[0]==list_index[i]:
				f2.write(line1)
for line5 in f5.readlines():
	if line5 == '\n':
		continue
	else:
		result_0 = line5.split()
		for i in range(len(list_index)):
			if result_0[0]==list_index[i]:
				f6.write(line5)
				#print(line5)

#训练模块
list2=[]
list_index_train=[]
for line3 in f3.readlines():
	if line3 == '\n':
		break
	else:
		result1=line3.split()
		list2.append(result1[1])
		if '|' in line3:
			#print(result1[1])
			list_index_train.append(result1[1])
for i in range(1,len(list2)):
	if list2[i]==list2[i-1]:
		#print(list2[i])
		list_index_train.append(list2[i])
#print(len(list_index_train))
list2_index=sorted(set(list_index_train))
print(len(list2_index))
f3=open('..\\data\汽车训练任务2.2改进.txt','r')
for line3 in f3.readlines():
	if line3 == '\n':
		break
	else:
		result_0 = line3.split()
		for i in range(len(list2_index)):
			if result_0[1]==list2_index[i]:
				f4.write(line3)
for line7 in f7.readlines():
	if line7 == '\n':
		continue
	else:
		result_0 = line7.split()
		#print(result_0[0])
		for i in range(len(list2_index)):
			if result_0[0]==list2_index[i]:
				f8.write(line7)
				#print(line7)





