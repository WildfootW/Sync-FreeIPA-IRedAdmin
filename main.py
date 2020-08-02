#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#   Version 
#   Author: WildfootW
#   GitHub: github.com/WildfootW
#   Copyleft (C) 2020 WildfootW All rights reversed.
#

from ldap3 import Server, Connection, ALL
import re
import queue
import config

server = Server(config.hostname, port = config.hostport, use_ssl = True, get_info = ALL)
conn = Connection(server, config.bindDN, config.bindPW, auto_bind = True)
# print(conn.entries[0]['member'])

# return members, group_content
def group_analysis(dn):
    conn.search(dn, "(objectClass=*)", attributes = ['cn', 'member'])
    return

# return members, user_content
def user_analysis(dn):
    return

group_dict = {}
user_dict = {}
dn_queue = queue.Queue()
conn.search(config.groupsDN, "(cn=mail_group)", attributes = ['member'])
map(dn_queue.put, conn.entries[0]['member'])
#for dn in conn.entries[0]['member']:
#    dn_queue.put(dn)

while not dn_queue.empty():
    dn_current = dn_queue.get()
    if dn_current[-len(groupsDN):]: # is group
        members, group_content = group_analysis(dn_current)
        map(dn_queue.put, members)
        group_dict[group_content['name']] = group_content
    elif dn_current[-len(usersDN):]: # is user
        members, user_content = user_analysis(dn_current)
        map(dn_queue.put, members)
        user_dict[user_content['name']] = user_content
    else:
        raise RuntimeError("Not user nor group")
