#!/usr/bin/env python
import SimpleHTTPServer
import BaseHTTPServer
import employees
import json
import re
import sys
import urllib
import urlparse

flag_db_filename='db.bak'
database=[]
flag_db={}

def load_flag_db():
	global flag_db_filename
	global flag_db
	try:
		flag_db_file=open(flag_db_filename,'r')
		flag_db=json.loads(flag_db_file.read())
		flag_db_file.close()
	except:
		pass

def save_flag_db():
	try:
		flag_db_file=open(flag_db_filename,'w')
		flag_db_temp=json.dumps(flag_db)
		flag_db_file.write(flag_db_temp)
		flag_db_file.close()
	except:
		pass

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		try:
			global database
			self.path='web/'+self.path
			query_str=urlparse.urlparse(self.path).query

			if len(query_str)==0:
				return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
			else:
				for query in query_str.split('&'):
					query=query.split('=')
					if len(query)>1:
						key=query[0]
						val=urllib.unquote(query[1])
						if key=='id':
							return SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
						if key=='search':
							val=re.sub('[^0-9a-zA-Z]+',' ',val).lower().split(' ')
							self.send_response(200)
							self.send_header('Content-type','text/html')
							self.end_headers()
							obj=employees.search(database,val,False,True)
							if len(obj)>2:
								obj_parsed=json.loads(obj)
								if len(obj_parsed)>0:
									if not val[0] in flag_db:
										flag_db[val[0]]='00000000'
									obj_parsed[0]['flags']=flag_db[val[0]]
									obj=json.dumps(obj_parsed)
							self.wfile.write(str(obj))
							self.wfile.close()
						if key=='flag':
							obj='{}'
							id=val[:6]
							num=val[6:]
							if len(num)>0:
								num=int(num)
							if len(id)==6 and num>=0 and num<=7:
								obj=employees.search(database,[id],False,True)
								if len(obj)>2:
									if not id in flag_db:
										flag_db[id]='00000000'
									flag_db[id]=flag_db[id][:num]+'1'+flag_db[id][num+1:]
									save_flag_db()
							self.send_response(200)
							self.send_header('Content-type','text/html')
							self.end_headers()
							self.wfile.write('')
							self.wfile.close()
		except Exception as error:
			self.send_response(400)
			self.end_headers()
			self.wfile.close()
			sys.stderr.write(str(error)+'\n')
			pass

if __name__=="__main__":
	try:
		load_flag_db()
		database=employees.load_from_csv('names.csv')
		Handler=MyHandler
		server=BaseHTTPServer.HTTPServer(('0.0.0.0',8081),MyHandler)
		server.serve_forever()
	except Exception as error:
		sys.stderr.write(str(error)+'\n')
		exit(1)
