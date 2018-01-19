# SYNOPSIS

Outthentic plugin. 

Get zabbix's hostnames by description of alerts.

Tested on zabbix 3.2+.

Python - 2.7
# INSTALL

    $ sparrow plg install zabbix-hosts-by-alerts

## Dependencies

[pyzabbix](https://github.com/lukecyca/pyzabbix)

# USAGE

## Manually
 
     $ sparrow plg run zabbix-hosts-by-alerts --param user=foo --param password=bar --param host=127.0.0.1 --param pattern="Server unreachable"
     
     test.tomatonetwork.ru
     test2.tomatonetworku.ru
# Parameters

## user
 
 A user to login. No default value. Obligatory.
 
## password
 
 A password. Obligatory.
 
## host
 
 IP of zabbix server. Obligatory.

## pattern
 
 Part of alert's description.

## output 

 Default is `stdout`. If any other specified output will be in file.

## severity

 Minimal severity of alert. Default is `3`

## duration

 Minimal duration for alert being in BAD state. Default is `5 minutes`

# See also

[sparrowdo](https://github.com/melezhik/sparrowdo)

[sparrow](https://github.com/melezhik/sparrow)
