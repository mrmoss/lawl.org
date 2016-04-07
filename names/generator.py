#!/usr/bin/env python
import hashlib
import sys

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
		self.username=(first[0]+last).lower()
		self.occupation=occupations[(ord(first[0])*ord(last[0]))%len(occupations)]
		self.occupation_num=-1
		for oo in range(0,len(occupation_nums)):
			if self.occupation==occupation_nums[oo]:
				self.occupation_num=(ord(occupation_nums[oo][0])+ord(occupation_nums[oo][1]))%99
		id_hash=hashlib.md5(first+last).hexdigest()
		self.id=22000000
		for ii in id_hash:
			self.id+=int(ii,16)**4

try:
	employees={}
	counts={}
	delim=','
	for oo in occupations:
		counts[oo]=0
	file=open('names_in.txt','r')
	for line in file:
		line=line.strip()
		line=line.split();
		if len(line)==2:
			employee=employee_t(line[0],line[1])
			employees[employee.id]=employee
	for ee in employees:
		print(str(employees[ee].id)+delim+
			str(employees[ee].occupation_num)+delim+
			str(employees[ee].occupation)+delim+
			employees[ee].first+delim+
			employees[ee].last+delim+
			employees[ee].username)
		counts[employees[ee].occupation]+=1
	sys.stderr.write('Total='+str(len(employees))+'\n')
	for cc in counts:
		sys.stderr.write(cc+'='+str(counts[cc])+'\n')
	exit(0)
except Exception as error:
	sys.stderr.write(str(error)+'\n')
	exit(1)
