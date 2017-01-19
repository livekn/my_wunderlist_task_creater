#!/usr/bin/env python
#coding: utf8
import json
import requests
import sys, getopt
import os.path
import datetime

def get_list(headers):
	lists = requests.get("https://a.wunderlist.com/api/v1/lists", headers=headers).json()

	for item in lists:
		print( str(item['id']) + " : " + item['title'] )

def usage():
	print( "Usage:\n" + sys.argv[0] + " get_list\n" + sys.argv[0] + " [ --due today/tomorrow/2038-01-19 ] [ --star ] [ --list list_id ] add task_name" )

def add_task(headers, task):
	result = requests.post( "https://a.wunderlist.com/api/v1/tasks", headers=headers, data=json.dumps(task) )

	if result.status_code != 201:
		print( result.text )

def main():
	if not( os.path.isfile("config.json") ):
		print("Please create config.json first.")
		sys.exit(2)

	config = json.loads( open("config.json").read() )
	headers = { 'X-Access-Token' : config['token'], 'X-Client-ID' : config['client_id'], 'Content-Type' : 'application/json' }
	
	try:
		opts, args = getopt.getopt( sys.argv[1:], "h", [ "due=", "star", "list="] )
	except getopt.GetoptError:
		usage()
		sys.exit(3)

	if not( args ):
		usage()
		sys.exit(3)
	elif args[0] == "get_list":
		get_list(headers)
	elif args[0] == "add":
		if len(args)<2:
			usage()
			sys.exit(3)
		task = { "title": args[1] }

		for opt, arg in opts:
			if opt == "--due":
				if arg == "today":
					day = datetime.date.today()
				elif arg == "tomorrow":
					day = datetime.date.today() + datetime.timedelta(days=1)
				else:
					try:
						day = datetime.date( int(arg.split('-')[0]), int(arg.split('-')[1]), int(arg.split('-')[2]) )
					except:
						print("Due day should be a valid day, like today is " + str(datetime.date.today()) + ".")
						sys.exit(4)
				task['due_date'] = str(day)
			elif opt == "--star":
				task['starred'] = True
			elif opt == "--list":
				task['list_id'] = int(arg)

		if not( config.get('default_list_id') ) and not( task.get('list_id') ):
			print( "Please give me your list id, you can set the default value at config.json." )
			sys.exit(5)
		task.setdefault( 'list_id', int( config.get('default_list_id') ) )
		
		add_task( headers, task )
	else:
		usage()
		sys.exit(3)

if __name__ == "__main__":
	main()
