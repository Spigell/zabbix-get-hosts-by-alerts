import ast
import sys
import logging
import re
import time

import oyaml as yaml
from outthentic import *
from pyzabbix import ZabbixAPI

output = config()['output']

def main():

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
    trigger_until = config()['duration']
    extended = config()['extended']
    with_values = config()['with_values']

    trigger_until_sec = int(trigger_until) * 60
    current_time = time.time()
    trigger_until_sec = current_time - trigger_until_sec

    zapi = ZabbixAPI(zhost)
    zapi.login(user, password)

    triggers = zapi.trigger.get(
        min_severity = min_severity,
        only_true = 'true',
        withLastEventUnacknowledged = 'true',
        lastChangeTill = trigger_until_sec
    )

    hostsinfo =''
    hostnames = ''
    trigger_ids=''
    for trigger in triggers:
        if trigger['value'] == '1':
            match = re.search(pattern, trigger['description'])
            if match:
                trigger_id = trigger['triggerid']

                if extended == 'true':

                    information = trigger['description']

                    host = zapi.host.get(
                        triggerids=(trigger_id)
                    )
                    hostname = host[0]['host'].encode('utf-8')

                    output_yaml = dict(
                        host = hostname
                    )

                    items = zapi.item.get(
                        triggerids=(trigger_id)
                    )
                    for index, item in enumerate(items):
                        value = item['lastvalue'] + item['units']

                        if len(items) > 1:
                            replace_pattern = re.compile('{' + 'ITEM.LASTVALUE' + str(index + 1) + '}')
                        else:
                            replace_pattern = re.compile("{ITEM.LASTVALUE}|{ITEM.LASTVALUE1}|{ITEM.VALUE}")


                        if with_values == 'true':
                            value_raw = item['lastvalue']
                            #.encode('utf-8')
                            key = 'value' + str(index)
                            output_yaml[key] = value_raw

                        information = re.sub(replace_pattern, value, information)
                        #.encode('utf-8')
                        output_yaml.update(alert = information)

                        info = yaml.safe_dump(output_yaml, encoding=('utf-8'), default_flow_style=False, allow_unicode=True)


                    hostsinfo += info + "\n"

                else: 
                    trigger_ids +=  trigger_id + ","

    if trigger_ids:

        trigger_ids=ast.literal_eval(trigger_ids)
        hosts = zapi.host.get(
            triggerids=(trigger_ids)
        )

        for host in hosts:
            hostname = host['host']
            hostnames += hostname + '\n'
        return hostnames

    elif hostsinfo:
        return hostsinfo

    else:
        return "Found nothing"




if __name__ == "__main__":
    result = main()

    if output == 'stdout':
        print(result)
    else:
        f = open(output, 'w')
        f.write(result)
        f.close()


