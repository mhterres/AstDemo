#!/usr/bin/python
# -*- coding: utf-8 -*-

# AstDemo_classes
#
# Marcelo H. Terres <mhterres@gmail.com>
# 2014-06-02
#
# Updated 2014/12/30

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
		time.sleep (0.1)
		data = s.recv(2048)

		self.socket = s

class ManagerDict:

	def __init__(self,text):

		activeLogs('/tmp','astdemo_classes','err')

		# split the text
		lines = text.split('\n')

		d={}

		for item in lines:

			data=item.split(":",1)

			try:

				title=data[0]
			except:

				title=""

			try:

				value=data[1]
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
		activeLogs('/tmp','astdemo_classes','err')

		# Read PGSql configuration and connect to there
		configuration = ConfigParser.RawConfigParser()
		configuration.read('%s/config.ini' % os.path.dirname(sys.argv[0]))

		# script
		self.path = os.path.dirname(sys.argv[0])
		self.version=configuration.get('general','version')

		# xmpp
		self.jid_auth=configuration.get('general','jid_auth')
		self.jid_pwd=configuration.get('general','jid_pwd')
		self.xmppdomain=configuration.get('general','xmppdomain')
		self.xmppresource=configuration.get('general','xmppresource')

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

		# asterisk
		self.asterisk_realtime=configuration.get('general','asterisk_realtime')
		self.asterisk_db_host=configuration.get('general','asterisk_db_host')
		self.asterisk_db_name=configuration.get('general','asterisk_db_name')
		self.asterisk_db_user=configuration.get('general','asterisk_db_user')
		self.asterisk_db_pwd=configuration.get('general','asterisk_db_pwd')
		self.asterisk_sip_table=configuration.get('general','asterisk_sip_table')
		self.asterisk_jid_field=configuration.get('general','asterisk_jid_field')

		# monitoring
		self.monitoring_log_operation=configuration.get('general','monitoring_log_operation')
		self.monitoring_log_state=configuration.get('general','monitoring_log_state')

		# call cmd
		self.call_callerid = configuration.get('general','call_callerid')
		self.call_context = configuration.get('general','call_context')

class XMPPp:

	def __init__(self):


		activeLogs('/tmp/','astdemo_classes','err')

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

		self.client = cl


class ManagerDictEvents:

	def __init__(self,text,myevent):

		self.description = "Generate dictionary of a specific event."

		activeLogs('/tmp','astdemo_classes','err')

		# split the text
		lines = text.split('\n')

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

			for myitem in lines:

				data=myitem.split(":",1)

				try:

					title=data[0]
				except:

					title=""

				try:

					value=data[1]
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

class Queue:

		def __init__(self,queue,agi):

				self.description = 'Queue status'

				activeLogs('/tmp','astdemo_classes','err')

				myConnect=connectAMI()
				s = myConnect.socket

				astdb=astDB(agi)
				self.astdb=astdb

				s.send('Action: QueueSummary\nQueue: ' + queue + '\n\n')
				time.sleep (0.1)

				data = s.recv(65536)

				if data.find('Queue: ' + queue) == -1:

						self.isavailable=False
				else:

						self.isavailable=True

						mgrdict=ManagerDict(data)

						self.name=queue
						self.loggedmembers=mgrdict.getitem('LoggedIn')
						self.availablemembers=mgrdict.getitem('Available')
						self.members=[]

				s.close

		def membersNumber(self):

				members=0

				myConnect=connectAMI()
				s = myConnect.socket

				s.send('Action: QueueStatus\nQueue: ' + self.name + '\n\n')
				time.sleep (0.1)

				data = s.recv(65536)
				mgrdict=ManagerDict(data)

				lines = data.split('\n')

				for item in lines:

						data=item.split(":",1)

						try:

								title=data[0]
						except:

								title=""

						if title == "Name":

								members = members + 1

				s.close

				return (members)


		def getmembers(self):

				myConnect=connectAMI()
				s = myConnect.socket

				s.send('Action: QueueSummary\nQueue: %s\n\n' % self.name)
				time.sleep (0.1)
				data = s.recv(65536)

				mgrdict=ManagerDict(data)

				self.loggedmembers=mgrdict.getitem('LoggedIn')
				self.availablemembers=mgrdict.getitem('Available')

				s.send('Action: QueueStatus\nQueue: ' + self.name + '\n\n')
				time.sleep (0.1)

				data2 = s.recv(65536)
				mgrdict=ManagerDict(data2)

				self.strategy = mgrdict.getitem('Strategy')
				self.calls = mgrdict.getitem('Calls')
				self.completed = mgrdict.getitem('Completed')
				self.abandoned = mgrdict.getitem('Abandoned')
				self.holdtime = mgrdict.getitem('Holdtime')
				self.talktime = mgrdict.getitem('TalkTime')

				lines = data2.split('\n')

				aMembers=[]

				for item in lines:

						data=item.split(":",1)

						try:

								title=data[0]
						except:

								title=""

						try:

								value=data[1]
						except:

								value=""

						if title == "Name":

								aMembers.append(value)

				self.members=[]

				self.members=aMembers

				s.close

				return (aMembers)

		def ismember(self,member):

				returnValue=False

				for item in self.members:

						if 'SIP/' + member in item:

								returnValue=True

				return returnValue

		def addmember(self,member,agi):

				myConnect=connectAMI()
				s = myConnect.socket

				if self.ismember(member):

						returnmsg = "Extension %s is already a queue %s member." % (member,self.name)
				else:

						s.send('Action: QueueAdd\nQueue: ' + self.name + '\nInterface: SIP/' + member + '\n\n')
						time.sleep(.2)

						self.getmembers()

						if self.ismember(member):

							self.astdb.put('queue',member,self.name)
							self.astdb.put('queuelogin',member,1)

							returnmsg = "Extension %s now is a member of queue %s." % (member,self.name)
						else:
	
							returnmsg = "Error: extension %s can't join queue %s." % (member,self.name)
							s.close()

				return (returnmsg)

		def removemember(self,member,agi):

				myConnect=connectAMI()
				s = myConnect.socket

				if not self.ismember(member):

					returnmsg = "Extension %s is not a queue %s member." % (member,self.name)

				else:

						s.send('Action: QueueRemove\nQueue: ' + self.name + '\nInterface: SIP/' + member + '\n\n')
						time.sleep(.2)

						self.getmembers()

						if not self.ismember(member):

								self.astdb.rem('queue',member)
								self.astdb.rem('queuelogin',member)

								returnmsg = "Extension %s leaves queue %s." % (member,self.name)
						else:

								returnmsg = "Error: extension %s can't leave queue %s." % (member,self.name)


				s.close()

				return (returnmsg)

class astDB():

	def __init__(self,agi):

		self.description = 'Asterisk Database'

		activeLogs('/tmp','astdemo_classes','err')

		self.agi=agi

	def get(self,key,extension):

		return self.agi.database_get("exten_%s" % extension, key)

	def put(self,key,extension,value):

		self.agi.database_put("exten_%s" % extension, key, value)

	def rem(self,key,extension):

		self.agi.database_del("exten_%s" % extension, key);

