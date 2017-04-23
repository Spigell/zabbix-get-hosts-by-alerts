import ast
import re
from outthentic import *
from pyzabbix import ZabbixAPI

zhost = config()['host']
user = config()['user']
password = config()['password']
pattern = config()['pattern']


zapi = ZabbixAPI(zhost)
zapi.login(user, password)
triggers = zapi.trigger.get(
        min_severity=3,
        only_true='True'
    )
trigger_ids=''
for trigger in triggers:
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

for host in hosts:

    print "%s" % (host['host'])
