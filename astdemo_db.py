#!/usr/bin/python

import re
import psycopg2
import psycopg2.extras
import sys
from astdemo_classes import Config
from astdemo_classes import activeLogs

class DB:

	def __init__(self):

		activeLogs('/tmp','astdemo_db','err')

		cfg = Config()

		dsn = 'dbname=%s host=%s user=%s password=%s' % (cfg.db_dbname, cfg.db_host, cfg.db_user, cfg.db_pwd)

		conn = psycopg2.connect(dsn)
		curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
		self.cursor = curs
		self.config = cfg

	def logMessage(self,msg_from,msg_to,msg_msg):

		sql = "BEGIN TRANSACTION; INSERT INTO logs VALUES(DEFAULT,DEFAULT,%s,%s,%s); COMMIT;"
		self.cursor.execute(sql, (msg_from,msg_to,msg_msg,))

	def monitorOperation(self,jid,operation,operation_type,operation_target):

		if operation=="monitor":

			if not self.monitorOperationExists(jid,operation,operation_type,operation_target):

				sql = "BEGIN TRANSACTION; INSERT INTO monitors VALUES(DEFAULT,DEFAULT,%s,%s,%s,%s); COMMIT;"
				self.cursor.execute(sql, (jid,operation,operation_type,operation_target))

				if self.config.monitoring_log_operation == "1":

					sql = "BEGIN TRANSACTION; INSERT INTO monitors_logs VALUES(DEFAULT,DEFAULT,%s,%s,%s,%s); COMMIT;"
					self.cursor.execute(sql, (jid,operation,operation_type,operation_target))

				return True

			else:

				return False

		else:

				if self.monitorOperationExists(jid,operation,operation_type,operation_target):

					sql = "BEGIN TRANSACTION; DELETE FROM monitors WHERE jid=%s AND operation='monitor' AND type=%s AND target=%s;COMMIT;"
					self.cursor.execute(sql, (jid,operation_type,operation_target))

					if self.config.monitoring_log_operation == "1":

						sql = "BEGIN TRANSACTION;INSERT INTO monitors_logs VALUES(DEFAULT,DEFAULT,%s,%s,%s,%s);COMMIT;"
						self.cursor.execute(sql, (jid,operation,operation_type,operation_target))

					return True

				else:

					return False

	def monitorOperationExists(self,jid,operation,operation_type,operation_target):

		sql = "SELECT * from monitors WHERE jid=%s AND operation='monitor' AND type=%s AND target=%s;"
		self.cursor.execute(sql, (jid,operation_type,operation_target))

		if not self.cursor.rowcount:

			return False
			
		return True

	def monitorUpdateState(self,jid,operation_type,operation_target,operation_state):

		if self.monitorOperationExists(jid,'monitor',operation_type,operation_target):

			sql = "BEGIN TRANSACTION;UPDATE monitors SET laststate=%s WHERE jid=%s AND operation='monitor' AND type=%s AND target=%s;COMMIT;"
			self.cursor.execute(sql, (operation_state,jid,operation_type,operation_target))

			if self.config.monitoring_log_state == "1":

				sql = "BEGIN TRANSACTION;INSERT INTO monitors_logs VALUES(DEFAULT,DEFAULT,'',%s,%s,%s,%s);COMMIT;"
				self.cursor.execute(sql, ('monitor',operation_type,operation_target,operation_state))

	def monitoringItems(self,jid):

		sql = "SELECT date,operation,type,target,laststate FROM monitors WHERE jid='%s';" % jid
		self.cursor.execute(sql)

		returnmsg=""

		if self.cursor.rowcount:

			for row in self.cursor:

					returnmsg+="%s - %s %s %s - last status: %s\r" % (row['date'],row['operation'].strip(),row['type'].strip(),row['target'].strip(),row['laststate'])

		return returnmsg

	def returnAllItems(self):

		sql = "SELECT * FROM monitors;"
		self.cursor.execute(sql)

		return (self.cursor)
