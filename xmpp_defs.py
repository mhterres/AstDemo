#!/usr/bin/python
# -*- coding: utf-8 -*-

# Defs
#
# Marcelo H. Terres <mhterres@gmail.com>
# 2014-06-02
#
# Versao 0.2.1.1

import socket
import time
import re
import psycopg2
import psycopg2.extras
import ConfigParser

from xmpp_classes import connectAMI
from xmpp_classes import activeLogs
from xmpp_classes import ManagerDict
from xmpp_classes import ManagerDictEvents

def sipPeer(sip):

	activeLogs('/tmp','xmpp_defs','err')

	myConnect=connectAMI()
	s = myConnect.socket

	s.send('Action: SIPshowpeer\nPeer: ' + sip + '\n\n')
	time.sleep (0.2)

	data = s.recv(65536)

	mgrdict=ManagerDict(data)

	returnmsg = "Extension %s informations: " % sip
	returnmsg += "\r"

	if data.find("Peer " + sip + " not found") > 0:

		returnmsg += "Ramal " + sip + " não registrado.\n"
	else:		
		returnmsg += "CallerID: " + mgrdict.getitem('Callerid') 
		returnmsg += "IP: " + mgrdict.getitem('Address-IP')
		returnmsg += "Codecs: " + mgrdict.getitem('Codecs')
		returnmsg += "Status: " + mgrdict.getitem('Status')
		returnmsg += "User Agent: " + mgrdict.getitem('SIP-Useragent')

	s.close()

	return returnmsg

def infoVoIP():

	activeLogs('/tmp','xmpp_defs','err')

	myConnect=connectAMI()
	s = myConnect.socket

	s.send('Action: CoreSettings\n\n')
	time.sleep (0.2)

	data = s.recv(65536)

	mgrdict=ManagerDict(data)

	returnmsg = "VoIP Informations"
	returnmsg += "\r"
	returnmsg += "Asterisk Version %s " % mgrdict.getitem('AsteriskVersion') 

	s.send('Action: CoreStatus\n\n')
	time.sleep (0.2)

	data = s.recv(65536)

	mgrdict=ManagerDict(data)

	returnmsg += "Started: " + mgrdict.getitem('CoreStartupDate').replace('\r','') + ' - ' + mgrdict.getitem('CoreStartupTime')
	returnmsg += "Last reload: " + mgrdict.getitem('CoreReloadDate').replace('\r','')  + ' - ' + mgrdict.getitem('CoreReloadTime')

	s.close()
	
	return returnmsg

def iaxPeers():

	myConnect=connectAMI()
	s = myConnect.socket

	s.send('Action: IAXpeers\n\n')
	time.sleep (0.2)

	data = s.recv(65535)

	mgrdictev=ManagerDictEvents(data,'PeerEntry')

	if not mgrdictev.isvalid:

		returnmsg = "IAX peers not found."
		return returnmsg
	
	else:

		returnmsg = "IAX peers Informations - %s peers found.\r" % str(mgrdictev.items) 

		for event in mgrdictev.events:


			returnmsg+="Peer: " + event['ObjectName'] 
			returnmsg+="Type: " + event['ChanObjectType'] 
			returnmsg+="IP: " + event['IPaddress'] 
			returnmsg+="Port: " + event['IPport'] 
			returnmsg+="Trunk: " + event['Trunk'] 
			returnmsg+="Status: " + event['Status'] 
			returnmsg += '\r'

	s.close()
	
	return returnmsg

def sipPeers():

	myConnect=connectAMI()
	s = myConnect.socket

	s.send('Action: SIPpeers\n\n')
	time.sleep (0.2)

	data = s.recv(65535)

	mgrdictev=ManagerDictEvents(data,'PeerEntry')

	if not mgrdictev.isvalid:

		returnmsg = "SIP peers not found."
		return returnmsg
	
	else:

		returnmsg = "SIP peers Informations - %s peers found.\r " % str(mgrdictev.items) 

		for event in mgrdictev.events:


			returnmsg+="Peer: " + event['ObjectName'] 
			returnmsg+="Type: " + event['ChanObjectType'] 
			returnmsg+="IP: " + event['IPaddress'] 
			returnmsg+="Port: " + event['IPport'] 
			returnmsg+="Video support: " + event['VideoSupport'] 
			returnmsg+="Realtime: " + event['RealtimeDevice'] 
			returnmsg+="Status: " + event['Status'] 
			returnmsg += '\r'

	s.close()
	
	return returnmsg

