#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#   Version 
#   Author: WildfootW
#   GitHub: github.com/WildfootW
#   Copyleft (C) 2020 WildfootW All rights reversed.
#

from ldap3 import Server, Connection, ALL
import config

#server = Server(config.hostname, get_info = ALL)
server = Server(config.hostname, port = config.hostport, use_ssl = True, get_info = ALL)
conn = Connection(server, config.bindDN, config.bindPW, auto_bind = True)
#conn.search(config.baseDN, "(&(objectclass=person)(uid=wildfootw))", attributes = ['sn', 'memberOf', 'objectclass', 'mail'])
#print(conn.entries[0]['memberOf'][0])
#conn.search("cn=test_users,cn=groups,cn=accounts,dc=ipa,dc=example,dc=com", "(objectClass=*)", attributes = "*")
#conn.search("uid=e1000110,cn=users,cn=accounts,dc=ipa,dc=example,dc=com", "(objectClass=*)", attributes = ["nsAccountLock"])
#conn.search(config.groupsDN, "(&(objectClass=*)(memberOf=cn=mail_group,cn=groups,cn=accounts,dc=ipa,dc=example,dc=com))", attributes = ["cn", "member"])
conn.search(config.usersDN, "(&(objectClass=*)(memberOf=cn=mail_group,cn=groups,cn=accounts,dc=ipa,dc=example,dc=com))", attributes = ["cn"])
print(conn.entries)

