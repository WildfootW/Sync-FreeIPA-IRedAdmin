#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#   Version 
#   Author: WildfootW
#   GitHub: github.com/WildfootW
#   Copyleft (C) 2020 WildfootW All rights reversed.
#

from ldap3 import Server, Connection, ALL
import config

#server = Server("freeipa.ipa.i.hoschoc.com", get_info = ALL)
server = Server(config.hostname, port = config.hostport, use_ssl = True, get_info = ALL)
conn = Connection(server, config.bindDN, config.bindPW, auto_bind = True)
conn.search(config.baseDN, "(&(objectclass=person)(uid=wildfootw))", attributes = ['sn', 'memberOf', 'objectclass'])
print(conn.entries[0]['memberOf'][0])


