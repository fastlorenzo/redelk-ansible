#!/bin/sh
#
# Part of RedELK
# Script to start enrichment process of data in elasticsearch
#
# Author: Lorenzo Bernardi / @fastlorenzo
#
# License : BSD3
#
# Version: 0.1
#

LOGFILE="/var/log/redelk/update_iplist.log"

# Check if there isnt an old process running, we dont want to run this in parallel
pgrep update_iplist.py > /dev/null
IPLISTUPDATE=$?
if [ $IPLISTUPDATE -eq 1 ]; then
    /usr/share/redelk/bin/update_iplist.py >> $LOGFILE 2>&1
    printf "`date +'%b %e %R'` IPList update script ran \n" >> $LOGFILE 2>&1
fi
