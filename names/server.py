#!/usr/bin/env python
import SimpleHTTPServer
import BaseHTTPServer
import employees
import re
import sys
import urllib
import urlparse

database=[]

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
							self.send_response(200)
							self.send_header('Content-type','text/html')
							self.end_headers()
							self.wfile.write(str(employees.search(database,val,False,True)))
							self.wfile.close()
		except Exception as error:
			self.send_response(400)
			self.end_headers()
			self.wfile.close()
			sys.stderr.write(str(error)+'\n')
			pass

if __name__=="__main__":
	try:
		database=employees.load_from_csv('names.csv')
		Handler=MyHandler
		server=BaseHTTPServer.HTTPServer(('0.0.0.0',8081),MyHandler)
		server.serve_forever()
	except Exception as error:
		sys.stderr.write(str(error)+'\n')
		exit(1)
