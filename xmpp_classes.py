#!/usr/bin/python
# -*- coding: utf-8 -*-

# Classes
#
# Marcelo H. Terres <mhterres@gmail.com>
# 2014-06-02
#
# Versao 0.2.1.1

import os
import sys
import xmpp
import time
import socket
import ConfigParser

class activeLogs:

	def __init__(self,direct,filename,typelog):

		log = open(direct + '/' + filename + '.log' , 'a')

		if typelog == 'err':

			sys.stderr = log

		elif typelog == 'out':

			sys.stdout = log

		elif typelog == 'all':

			sys.stderr = log
			sys.stdout = log

class connectAMI:

	def __init__(self):

		myConfigs = Config()

		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((myConfigs.voip_manager_srv,5038))

		s.send('Action: Login\nUsername: '+myConfigs.voip_manager_usr+'\nSecret: '+myConfigs.voip_manager_pwd+'\nEvents: off\n\n')
		time.sleep (0.2)
		data = s.recv(2048)

                self.socket = s

class ManagerDict:

	def __init__(self,text):

		activeLogs('/tmp','xmpp_classes','err')

		# split the text
		linhas = text.split('\n')

		d={}

		for item in linhas:

			dado=item.split(":",1)

			try:

				title=dado[0]
			except:

				title=""

			try:

				value=dado[1]
			except:

				value=""


			d.update({title:value})

		self.dicti=d

	def getitem(self,index):

		i=self.dicti[index]
		i=i.replace(" ","\ ")
		return i

class Config:

	def __init__(self):

		self.description = 'AstDemo configurations'
		activeLogs('/tmp','xmpp_classes','err')

		# Read PGSql configuration and connect to there
		configuration = ConfigParser.RawConfigParser()
		configuration.read('%s/config.ini' % os.path.dirname(sys.argv[0]))

		# script
		self.version=configuration.get('general','version')

		# xmpp
		self.jid_auth=configuration.get('general','jid_auth')
		self.jid_pwd=configuration.get('general','jid_pwd')

		# voip
		self.voip_manager_srv=configuration.get('general','voip_manager_srv')
		self.voip_manager_usr=configuration.get('general','voip_manager_usr')
		self.voip_manager_pwd=configuration.get('general','voip_manager_pwd')

		# db
		self.db_host=configuration.get('general','db_host')
		self.db_dbname=configuration.get('general','db_dbname')
		self.db_user=configuration.get('general','db_user')
		self.db_pwd=configuration.get('general','db_pwd')

		# serverinfo
		self.serverinfo_host=configuration.get('general','serverinfo_host')
		self.serverinfo_port=configuration.get('general','serverinfo_port')
	
class XMPPp:

	def __init__(self):


		activeLogs('/tmp/','xmpp_classes','err')

		myConfigs=Config()

		jid = xmpp.protocol.JID(myConfigs.jid_auth)

		self.domain=jid.getDomain()
		self.node=jid.getNode()

		cl=xmpp.Client(self.domain,debug=[])
		con=cl.connect()

		if not con:

			self.connected=False
		else:

			self.connected=True

			auth=cl.auth(self.node,myConfigs.jid_pwd)

			if not auth:

				self.authenticated=False

			else:

				self.authenticated=True


class ManagerDictEvents:

	def __init__(self,text,myevent):

		self.description = "Generate dictionary of a specific event."

		activeLogs('/tmp','xmpp_classes','err')

		# split the text
		linhas = text.split('\n')

		i=0

		dicio={}
		events=[]

		fulldicio={}
		dicioitem=0

		if text.find('Event: ' + myevent) == -1:

			self.isvalid=False
		else:

			self.isvalid=True

			self.events=[]
			self.items=0
			self.fulldicti={}
			self.dictiitems=0

			for myitem in linhas:

				dado=myitem.split(":",1)

				try:

					title=dado[0]
				except:

					title=""

				try:

					value=dado[1]
				except:

					value=""

				if (title == "Event" and value.find(myevent) > 0 and len(dicio) == 0):

					i+=1
					events.append({})
					dicioitem+=1
					fulldicio.update({title:value})

					dicio.update({title:value})
					events[i-1].update({title:value})
			
				elif (title == "Event" and len(dicio)>0):

					dicioitem+=1
					fulldicio.update({title:value})

					if len(dicio) > 0:

						events[i-1].update({title:value})

						dicio.clear()
						dicio={}

					if value.find(myevent) > 0:

						i+=1
						events.append({})
						dicioitem+=1
						fulldicio.update({title:value})
						
						events[i-1].update({title:value})
						dicio.update({title:value})

				elif (title != "" and len(dicio)>0):

					dicioitem+=1
					fulldicio.update({title:value})

					events[i-1].update({title:value})
					dicio.update({title:value})

			self.items=i
			self.events=events
			self.dicti=fulldicio
			self.dictiitems=dicioitem
			self.text=text


