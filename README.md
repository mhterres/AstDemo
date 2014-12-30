AstDemo
=======

XMPP + VoIP (Openfire + Asterisk) demo integration.

Requisites
**********
* Openfire running
* Asterisk 11 or later running with XMPP support
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
* Edit your extensions.conf file, adding [from_xmpp_demo] context, [call] context and adding variables in [globals] context. If you want support to features like callerid and dnd, adapt your extensions context too. See extensions.conf file in asterisk_config directory.

Available Commands
******************
* callmsg <number> - make a call to <number> and play tt-monkeys when answered.
* callerid <extension> [jid] - enable or disable the callerid xmpp message on received calls to extension.
* info <voip|xmpp> - show VoIP or XMPP server informations.
* help - show this help.
* iaxpeers - show IAX peers.
* monitor iax <peer> - monitor iax <peer> state.
* monitor sip <extension> - monitor <extension> state.
* monitor queue <queue> - monitor queue <queue> and alarm when it has no members logged.
* monitoring - show monitoring items.
* sippeer <extension> - show SIP informations of <extension>.
* sippeers - show SIP peers.
* unmonitor iax <peer> - unmonitor iax <peer> state.
* unmonitor sip <extension> - unmonitor <extension> state.
* unmonitor queue <queue> - unmonitor queue <queue>.
* version - show astdemo version.

If you have Asterisk Realtime enabled you'll have access to more commands:
* call <sip extension> - call to <sip extension> and transfer to your extension when answered.
* dnd <on|off|status> - enable/disable or show Do Not Disturb status.
* queue <queue> - show <queue> members and statistics.
* queuemsg <queue> <message> - send <message> to all members of <queue>.
* enter <queue> - join <queue>.
* leave <queue> - leave <queue>.
* whoami - show informations about myself.

Asterisk Realtime Support
*************************
First question: do you have Asterisk Realtime enabled? Read more about Asterisk Realtime Architecture in https://wiki.asterisk.org/wiki/display/AST/Realtime+Database+Configuration. After your Asterisk have Realtime support, you can continue.

To activate Asterisk Realtime support in AstDemo, first you need to have a jid field in your sip database table (jid, character varying, length 150). 
If you have it, you just need to enable asterisk realtime support in config.ini file. 

If you activate Asterisk Realtime support in AstDemo you will release more AstDemo features.

After Asterisk Realtime support activation you will see new commands in help and some commands will change, like callerid, cause you don't need to indicate your extension and your jid anymore, it'll just toggle xmpp message. 

ATTENTION: you need to configure your sip record with your jid, or new resources will not work.

Monitoring
**********
To activate monitoring copy the cronjob file (cron/astdemo_monitor) to /etc/cron.d. 
To monitor IAX or SIP devices you need to qualify peer in its configuration (qualify=yes)
