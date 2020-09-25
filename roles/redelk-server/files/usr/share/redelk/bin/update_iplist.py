#!/usr/bin/python3
# version: 11 december 2018  v02
#
# Part of RedELK
# Script to start enrichment process of data in elasticsearch
#
# Author: Outflank B.V. / Mark Bergman / @xychix
# Modified: Lorenzo Bernardi / @fastlorenzo
#
# License : BSD3
#
# Version: 0.8
#
from elasticsearch import Elasticsearch
# from pprint import pprint
import json
import sys
import datetime
import netaddr
es  = Elasticsearch()

def pprint(r):
 print(json.dumps(r, indent=2, sort_keys=True))

import socket
def isIP(addr):
  try:
    socket.inet_aton(addr)
    # legal
    return(True)
  except socket.error:
    # Not legal
    return(False)

# Get all IPs for a specific list from ES
def getIPListFromES(ipList):
    # print("Getting %s from ES" % (ipList))
    q2 = {'query': {'query_string': {'query': 'FILLME'}}}
    q2['query']['query_string']['query'] = "type:\"%s\"" % ipList
    r2 = es.search(index='iplist_*', body=q2, size=10000)
    b = r2['hits']['hits']
    resIPList = []
    for doc in b:
        resIPList.append(doc['_source']['ip'])
    return(resIPList)

# Get all IPs for a specific list from config file
def getIPListFromConfig(ipList):
    configFile = '/etc/redelk/iplist_%s.conf' % ipList
    with open(configFile) as f:
      content = f.readlines()
    ipListList = []
    for line in content:
     if not line.startswith('#'):
       ip = line.strip()
       if isIP(ip):
         ipListList.append(line.strip())
    return(ipListList)

# Deletes an IP from ES
# Example: addIPToES('customer','127.0.0.2')
def addIPToES(ipList, ip):
    print('Adding IP %s to %s in ES' % (ip, ipList))
    doc = {
        'type': ipList,
        'ip': ip,
        '@timestamp': datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    }
    ip_obj = netaddr.IPAddress(ip)
    es.index(index='iplist_%s' % ipList, doc_type='_doc', id=ip_obj.value, body=doc)

# Deletes an IP from ES
# Example: delIPFromES('customer','127.0.0.2')
def delIPFromES(ipList, ip):
    print('Deleting IP %s from %s in ES' % (ip, ipList))
    ip_obj = netaddr.IPAddress(ip)
    es.delete(index='iplist_%s' % ipList, doc_type='post', id=ip_obj.value)

def syncESAndConfig(ipList):
    ipList_es = getIPListFromES(ipList)
    ipList_cfg = getIPListFromConfig(ipList)
    # pprint(ipList_es)
    # pprint(ipList_cfg)

    for ic in ipList_cfg:
        if ic not in ipList_es:
            addIPToES(ipList, ic)

    for ie in ipList_es:
        if ie not in ipList_cfg:
            delIPFromES(ipList, ie)

#### main
if __name__ == '__main__':
    ipLists = [
        'customer',
        'redteam',
        'unknown',
        'torexitnodes'
    ]
    for ipList in ipLists:
        print("Summary: date: %s, ipList: %s" % (datetime.datetime.now(), ipList))
        syncESAndConfig(ipList)
