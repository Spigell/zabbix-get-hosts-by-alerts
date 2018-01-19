import ast
import sys
import logging
import re
import time

from outthentic import *
from pyzabbix import ZabbixAPI


debug = config()['debug']

if debug == '1':

    stream = logging.StreamHandler(sys.stdout)
    stream.setLevel(logging.DEBUG)
    log = logging.getLogger('pyzabbix')
    log.addHandler(stream)
    log.setLevel(logging.DEBUG)

zhost = config()['host']
user = config()['user']
password = config()['password']
pattern = config()['pattern']
min_severity = config()['severity']
output = config()['output']
trigger_until = config()['duration']

trigger_until = int(trigger_until) * 60
current_time = time.time()

trigger_until = current_time - trigger_until

zapi = ZabbixAPI(zhost)
zapi.login(user, password)
triggers = zapi.trigger.get(
        min_severity = min_severity,
        only_true='True',
        withLastEventUnacknowledged = 'True',
        lastChangeTill = trigger_until
    )

trigger_ids=''
for trigger in triggers:
    if trigger['value'] == '1':
        triggersids = re.search(pattern, trigger['description'])
        if triggersids:
            trigger_id = (trigger['triggerid'])
            trigger_ids +=  trigger_id + ","

try:
    trigger_ids=ast.literal_eval(trigger_ids)
except SyntaxError:
    print "Found nothing"

zapi = ZabbixAPI(zhost)
zapi.login(user, password)
hosts = zapi.host.get(
    triggerids=(trigger_ids)
    )

if output == 'stdout':
    for host in hosts:
        print "%s" % (host['host'])
else:
    f = open(output, 'w')
    for host in hosts:
        f.write( "%s\n" % (host['host']))
    f.close()

