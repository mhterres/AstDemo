AstDemo
=======

XMPP + VoIP (Openfire + Asterisk) demo integration.

Requisites
**********
* Openfire running
* Asterisk running with XMPP support
* PostgreSQL running
* ServerInfo Plugin Support (http://www.mundoopensource.com.br/serverinfo-plugin-openfire/)
* python-pyst (http://sourceforge.net/projects/pyst/)
* python psycopg2 (http://initd.org/psycopg/)

Installation
************
* Create a subdirectory in your agi-bin asterisk dir named astdemo
* Put all astdemo files there
* Create you astdemo database (you can use db/pgsql/astdemo.sql)
* Copy config.ini.sample to config.ini and update inifile with your data
* Configure your xmpp Asterisk resource (asterisk_config/xmpp.conf has a sample of configuration)
* Edit your extensions.conf file, adding [from_xmpp_demo] context and adding variables in [globals] context. If you want support to features like callerid and dnd, adapt your extensions context too. See extensions.conf file in asterisk_config directory.

Available Commands
******************
* call <number> - make a call to <number> and play tt-monkeys when answered.
* callerid <extension> [jid] - enable or disable the callerid xmpp message on received calls to extension.
* info <voip|xmpp> - show VoIP or XMPP server informations.
* help - show this help.
* iaxpeers - show IAX peers.
* queuemsg <queue> <message> - send <message> to all members of <queue> (asterisk realtime required).
* sippeer <extension> - show SIP informations of <extension>.
* sippeers - show SIP peers.
* version - show astdemo version.
* whoami - show informations about myself (asterisk realtime required)

If you have Asterisk Realtime enabled you'll have access to more commands:
* dnd <on|off|status> - enable/Disable or show Do Not Disturb status.
* queue <queue> - show <queue> members and statistics.
* queuemsg <queue> <message> - send <message> to all members of <queue>.
* queueon <queue> - join <queue>.
* queueoff <queue> - leave <queue>.
* whoami - show informations about myself.

Asterisk Realtime Support
*************************

If you activate Asterisk Realtime support you will release more AstDemo features.

To activate Asterisk Realtime support in AstDemo, first you need to have a jid field in your sip database table (jid, character varying, length 150). 
If you have it, you just need to enable asterisk realtime support in config.ini file. 

After Asterisk Realtime support activation you will see new commands in help and some commands will change, like callerid, cause you don't need to indicate your extension and your jid anymore, it'll just toggle xmpp message. 

ATTENTION: you need to configure your sip record with your jid, or new resources will not work.
