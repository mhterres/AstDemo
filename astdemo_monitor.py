#!/usr/bin/python
# -*- coding: utf-8 -*-

# AstDemo_monitor
# Monitoring script
#
# Marcelo H. Terres <mhterres@gmail.com>
# 2014-12-30
#

import xmpp

from asterisk import agi

from astdemo_defs import iaxPeerStatus
from astdemo_defs import sipPeerStatus
from astdemo_defs import getQueueMembersNumber

from astdemo_db	import DB
from astdemo_classes import XMPPp
from astdemo_classes import Config
from astdemo_classes import activeLogs

activeLogs('/tmp','astdemo_monitor','all')

db=DB()
cfg=Config()

xmppdomain = cfg.xmppdomain
xmppresource = cfg.xmppresource

myXMPP=XMPPp()

db_cursor=db.returnAllItems()

totalRows=db_cursor.rowcount

print "-----------"

if totalRows:

	print "%i items monitored." % totalRows

	x = 1

	rows=db_cursor.fetchall()

	for row in rows:
	
		jid=row['jid'].strip()
		op_type=row['type'].strip()
		op_target=row['target'].strip()
		laststate=row['laststate']

		print "Processing row %i - %s %s" % (x,op_type,op_target)

		x = x + 1

		if op_type=="sip":

			state=sipPeerStatus(op_target).strip()
			message="SIP %s is now %s." % (op_target,state)

		elif op_type=="iax":

			state=iaxPeerStatus(op_target).strip()
			message="IAX %s is now %s." % (op_target,state)

		elif op_type=="queue":

			members=getQueueMembersNumber(op_target)

			if members==0:

				state="no members"
			else:

				state="%i member(s)" % members

			message="Queue %s now has %s." % (op_target,state)

		print state
		if laststate != state:

				db.monitorUpdateState(jid,op_type,op_target,state)
				myXMPP.client.send(xmpp.protocol.Message(jid,message))


