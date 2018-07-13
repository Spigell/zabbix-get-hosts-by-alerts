set_spl %( 'dev-zabbix-hosts-by-alerts' => 'https://github.com/spigell/zabbix-hosts-by-alerts.git' );

package-install 'git';

bash 'sparrow plg install dev-zabbix-hosts-by-alerts';
