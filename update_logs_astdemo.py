#!/usr/bin/python

import re
import psycopg2
import psycopg2.extras
import sys
from xmpp_classes import Config
from xmpp_classes import activeLogs

activeLogs('/tmp','update_logs_astdemo','err')

cfg = Config()

dsn = 'dbname=%s host=%s user=%s password=%s' % (cfg.db_dbname, cfg.db_host, cfg.db_user, cfg.db_pwd)

conn = psycopg2.connect(dsn)
curs = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


msg_from=sys.argv[1]
msg_to=sys.argv[2]
msg_msg=sys.argv[3]

sql = "BEGIN TRANSACTION; INSERT INTO logs VALUES(DEFAULT,DEFAULT,%s,%s,%s); COMMIT;"
curs.execute(sql, (msg_from,msg_to,msg_msg,))
conn.close()
