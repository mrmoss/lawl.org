#!/usr/bin/env python
import hashlib

occupations=[
	'HR',
	'AC',
	'MG',
	'HR',
	'AC',
	'MG',
	'HR',
	'AC',
	'MG',
	'HR',
	'AC',
	'MG',
	'HR',
	'AC',
	'MG',
	'HR',
	'AC',
	'MG',
	'HR',
	'HR',
	'HR',
	'SC',
	'IT',
	'JA']

occupation_nums=[
'MG',
'HR',
'AC',
'JA',
'SC',
'IT'
]

class employee_t:
	def __init__(self,first,last):
		self.first=first
		self.last=last
		self.occupation=occupations[(ord(first[0])*ord(last[0]))%len(occupations)]
		self.occupation_num=-1
		for oo in range(0,len(occupation_nums)):
			if self.occupation==occupation_nums[oo]:
				self.occupation_num=oo
		id_hash=hashlib.md5(first+last).hexdigest()
		self.id=22000000
		for ii in id_hash:
			self.id+=int(ii,16)**4

try:
	employees={}
	counts={}
	for oo in occupations:
		counts[oo]=0
	file=open('names.txt','r')
	for line in file:
		line=line.strip()
		line=line.split();
		if len(line)==2:
			employee=employee_t(line[0],line[1])
			employees[employee.id]=employee
	for ee in employees:
		print(str(employees[ee].id)+' '+str(employees[ee].occupation)+' 0'+str(employees[ee].occupation_num)+' '+employees[ee].first+' '+employees[ee].last)
		counts[employees[ee].occupation]+=1
	print('Total='+str(len(employees)))
	for cc in counts:
		print(cc+'='+str(counts[cc]))
	exit(0)
except Exception as error:
	print(error)
	exit(1)
