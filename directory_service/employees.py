#!/usr/bin/env python2
import hashlib
import json

departments=[
	('MG',49,'Management'),
	('HR',55,'Human Resources'),
	('AC',33,'Accounting'),
	('JA',40,'Janitorial'),
	('SC',51,'Security'),
	('IT',58,'Information Technology')]

class department_t:
	def __init__(self,data=None):
		global departments
		self.initials='NA'
		self.number=0
		self.name="Invalid"
		if type(data)==str:
			if len(data)==2:
				for department in departments:
					if department[0]==data:
						self.initials=department[0]
						self.number=department[1]
						self.name=department[2]
			else:
				for department in departments:
					if department[2]==data:
						self.initials=department[0]
						self.number=department[1]
						self.name=department[2]
		if type(data)==int:
			for department in departments:
				if department[1]==data:
					self.initials=department[0]
					self.number=department[1]
					self.name=department[2]

class employee_t:
	def __init__(self,first=None,last=None):
		if first!=None and last!=None:
			self.first=first
			self.last=last
			self.username=(self.first[0]+self.last).lower()

	def json(self,authorized=False,ordered=False):
		obj={}
		prefix=''
		if ordered:
			prefix=0
		obj[str(prefix)+'Full Name']=self.first+" "+self.last
		if ordered:
			prefix+=1
		obj[str(prefix)+'First Name']=self.first
		if ordered:
			prefix+=1
		obj[str(prefix)+'Last Name']=self.last
		if ordered:
			prefix+=1
		obj[str(prefix)+'Email']=self.username+'@lawl.org'
		if ordered:
			prefix+=1
		obj[str(prefix)+'Department']=self.department.name
		if ordered:
			prefix+=1
		if authorized:
			obj[str(prefix)+'ID']=self.id
			if ordered:
				prefix+=1
			obj[str(prefix)+'Username']=self.username
			if ordered:
				prefix+=1
			obj[str(prefix)+'Department Number']=self.department.number
			if ordered:
				prefix+=1
			obj[str(prefix)+'Department Initials']=self.department.initials
			if ordered:
				prefix+=1
			obj[str(prefix)+'Issue Number']=self.issue
		return obj

	def csv(self,authorized=False):
		csv=''
		delim=','
		csv+=str(self.id)+delim
		csv+=str(self.department.number)+delim
		csv+=self.department.initials+delim
		csv+=str(self.issue)+delim
		csv+=self.first+delim
		csv+=self.last+delim
		csv+=self.username+delim
		csv+=self.department.name
		return csv

	def arr(self,authorized=False):
		arr=[]
		arr.append(self.first.lower())
		arr.append(self.last.lower())
		arr.append(str(self.id).lower())
		arr.append(self.username.lower())
		return arr

def search(database,terms,authorized=False,ordered=False):
	results=[]
	for term in terms:
		if len(term)>3:
			for employee in database:
				values=employee.arr()
				for ii in range(len(values)):
					if (ii<2 and term in values[ii]) or term==values[ii]:
						results.append(employee.json(authorized,ordered))
						break
	return str(json.dumps(results))

def gen_from_names(filename):
	database=[]
	delim=','
	file=open(filename,'r')
	for line in file:
		line=line.strip()
		line=line.split();
		if len(line)==2:
			database.append(employee_t(line[0],line[1],True))
	return database

def load_from_csv(filename):
	database=[]
	file=open(filename,'r')
	for line in file:
		line=line.strip()
		line=line.split(',')
		if len(line)==8:
			employee=employee_t()
			employee.id=line[0]
			employee.department=department_t()
			employee.department.number=zero_padded_int(line[1])
			employee.department.initials=line[2]
			employee.issue=zero_padded_int(line[3])
			employee.first=line[4]
			employee.last=line[5]
			employee.username=line[6]
			employee.department.name=line[7]
			database.append(employee)
	return database

def zero_padded_int(string):
	ii=str(string).strip().lstrip('0')
	if len(ii)==0:
		ii='0'
	return int(ii)
