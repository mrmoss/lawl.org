#!/usr/bin/env python
import SimpleHTTPServer
import BaseHTTPServer
import json
import re
import sys
import urllib
import urlparse

database=[]

def search_db(terms):
	global database
	found=[]
	for ii in terms:
		if len(ii)>3:
			for jj in range(0,len(database)):
				for kk in range(0,len(database[jj])):
					check=database[jj][kk].lower()
					if kk!=1 and ((kk!=0 and kk!=6 and ii in check) or (kk==0 and ii==check)):
						found.append({
						'0Full Name':database[jj][3]+" "+database[jj][4],
						'1First Name':database[jj][3],
						'2Last Name':database[jj][4],
						'3Email':database[jj][5]+'@lawl.org',
						'4Department':database[jj][6]})
						break
	json_obj=json.dumps(found)
	return str(json_obj)

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
						if key=='search':
							val=re.sub('[^0-9a-zA-Z]+',' ',val).lower().split(' ')
							found=search_db(val)
							self.send_response(200)
							self.send_header('Content-type','text/html')
							self.end_headers()
							self.wfile.write(str(found))
							self.wfile.close()
		except Exception as error:
			sys.stderr.write(str(error)+'\n')
			pass

try:
	file=open('names_out.txt','r')
	for line in file:
		line=line.strip()
		line=line.split(',')
		if len(line)==7:
			database.append(line)
	Handler=MyHandler
	server=BaseHTTPServer.HTTPServer(('127.0.0.1',8080),MyHandler)
	server.serve_forever()
except Exception as error:
	sys.stderr.write(str(error)+'\n')
	exit(1)