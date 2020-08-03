#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#   Version 
#   Author: WildfootW
#   GitHub: github.com/WildfootW
#   Copyleft (C) 2020 WildfootW All rights reversed.
#

from ldap3 import Server, Connection, ALL
import re
import config

server = Server(config.hostname, port = config.hostport, use_ssl = True, get_info = ALL)
conn = Connection(server, config.bindDN, config.bindPW, auto_bind = True)

def is_group(dn):
    return dn[-len(config.groupsDN):] == config.groupsDN

def is_user(dn):
    return dn[-len(config.usersDN):] == config.usersDN

conn.search(config.groupsDN, "(&(objectClass=*)(memberOf=" + config.mailGroupDN + "))", attributes = ['cn', 'member'])


