AstDemo
=======

XMPP + VoIP (Openfire + Asterisk) demo integration.

Requisites
**********
Openfire running
Asterisk running with XMPP support
PostgreSQL running
ServerInfo Plugin Support (http://www.mundoopensource.com.br/serverinfo-plugin-openfire/)
python-pyst (http://sourceforge.net/projects/pyst/)
python psycopg2 (http://initd.org/psycopg/)

Installation
************
* Create a subdirectory in yout agi-bin asterisk dir named astdemo
* Put all astdemo files there
* Create you astdemo database (you can use db/pgsql/astdemo.sql)
* Copy config.ini.sample to config.ini and update inifile with your informations
* Configure your xmpp Asterisk resource (xmpp.conf has a sample of configuration)
* Edit your extensions.conf file, adding [from_xmpp_demo] context and adding variables in [globals] context. See extensions.conf file provided with astdemo.

Available Commands
******************
* call <number> - Make a call to <number> and play tt-monkeys.
* info <voip|xmpp> - show VoIP or XMPP server informations.
* help - show this help.
* iaxpeers - show IAX peers.
* sippeer <extension> - show SIP informations of <extension>.
* sippeers - show SIP peers.
* version - show astdemo version.
