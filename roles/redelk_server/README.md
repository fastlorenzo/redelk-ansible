# redelk-server

Ansible role to deploy [RedELK](https://github.com/outflanknl/RedELK/) server components.

## Variables

The following variables can be modified:

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| certs_dir_nginx | string | `"/etc/nginx/certs"` | Path to folder containing certificates in Nginx container |
| certs_dir_nginx_ca | string | `"/etc/nginx/ca_certs"` | Path to folder containing the CA certificate in Nginx container |
| certs_dir_nginx_ca_local | string | `"./mounts/certs/ca"` | Local path to folder containing the CA certificate |
| certs_dir_nginx_local | string | `"./mounts/certbot/conf/live/localhost"` | Local path to folder containing certificates. Replace `localhost` with the same value as `external_domain` |
| customer_ips | list | `[]` | List of customer's IP addresses |
| docker_dir | string | `"/var/lib/docker"` | Docker directory |
| domains | list | `[]` | List of domain names used for the exercise |
| es_elastic_password | string | `"elastic"` | ElasticSearch users |
| es_kibana_encryptionKey | string | `"sLOVUK5MLv0VDhKsMlQcjgAaSMLXLLVy"` | Kibana encryption key (32 char alphanumeric) |
| es_kibana_password | string | `"kibana"` | ElasticSearch `kibana` user's password |
| es_logstash_system_password | string | `"logstash_system"` | ElasticSearch `logstash_system` user's password |
| es_redelk_ingest_password | string | `"redelk"` | ElasticSearch redelk-ingest user's password (used by logstash) |
| es_redelk_password | string | `"redelk"` | ElasticSearch RedELK user's password |
| es_redelk_user | string | `"redelk"` | ElasticSearch RedELK username |
| es_version | string | `"7.16.3"` | Elastic version |
| external_domain | string | `"localhost"` | External domain name to expose RedELK interface on. Will also be used to request Let's Encypt certificate |
| le_email | string | `""` | Let's Encrypt email address |
| le_enable | bool | `true` |  |
| le_staging | int | `0` | Set to `1` to use Let's Encrypt staging endpoint. |
| monitor_hosts | bool | `false` | Set to true to support monitoring hosts (metricbeat, packetbeat, ...) |
| neo4j_password | string | `"BloodHound"` | Neo4J password (user: neo4j) |
| optsec_dir | string | `"/opt"` | Base directory for components install (where customer data will be stored) - allows to store on an encrypted partition/disk |
| redelk_alarm_interval | string | `"3600"` |  |
| redelk_alarm_tempDir | string | `"/tmp"` |  |
| redelk_alarms | object | cf. below | Alarm configuration options |
| redelk_alarms.alarm_dummy.enabled | bool | `false` | Wether to enable the alarm |
| redelk_alarms.alarm_dummy.interval | int | `300` | Interval at which the alarm will run (in seconds) |
| redelk_alarms.alarm_filehash.enabled | bool | `true` | Wether to enable the alarm |
| redelk_alarms.alarm_filehash.ha_api_key | string | `"<<INSERT_API_KEY>>"` | Hybrid Analysis API key |
| redelk_alarms.alarm_filehash.ibm_basic_auth | string | `"Basic <<REPLACE>>"` | IBM X-Force Exchange basic authentication |
| redelk_alarms.alarm_filehash.interval | int | `360` | Interval at which the alarm will run (in seconds) |
| redelk_alarms.alarm_filehash.vt_api_key | string | `"<<INSERT_API_KEY>>"` | VirusTotal API key |
| redelk_alarms.alarm_httptraffic.enabled | bool | `true` | Wether to enable the alarm |
| redelk_alarms.alarm_httptraffic.interval | int | `310` | Interval at which the alarm will run (in seconds) |
| redelk_alarms.alarm_httptraffic.notify_interval | int | `86400` | Only notify on the same IP hit at every `notify_interval` (in seconds) |
| redelk_alarms.alarm_useragent.enabled | bool | `true` | Wether to enable the alarm |
| redelk_alarms.alarm_useragent.interval | int | `320` | Interval at which the alarm will run (in seconds) |
| redelk_cert_path | string | `"certificates/redelk"` | Local path to store RedELK certificates |
| redelk_client_connection_mode | string | `"reverse"` | Sets how RedELK clients connects to filebeat `direct` (client connects to RedELK server IP directly) or `reverse` (reverse SSH tunnel is made from RedELK server to clients) |
| redelk_enrich | object | cf. below | Settings for data enrichment. You can keep these enabled even if you don't use a specific item.  |
| redelk_enrich.enrich_csbeacon | object | cf. below | Enriches rtops data from Cobalt Strike implants. |
| redelk_enrich.enrich_csbeacon.enabled | bool | `true` | Wether to enable the enrichment module |
| redelk_enrich.enrich_csbeacon.interval | int | `300` | Interval (in seconds) at which the enrichment script will run |
| redelk_enrich.enrich_greynoise | object | cf. below | Enriches redirtraffic data with info from Greynoise. If an IP address is listed in Greynoise, this data is added. |
| redelk_enrich.enrich_greynoise.cache | int | `86400` | How long the data will be cached (in seconds). If an IP was already seen within this period, a new call to GeryNoise API will not be made. |
| redelk_enrich.enrich_greynoise.enabled | bool | `true` | Wether to enable the enrichment module |
| redelk_enrich.enrich_greynoise.interval | int | `310` | Interval (in seconds) at which the enrichment script will run |
| redelk_enrich.enrich_iplists | object | cf. below | Background RedELK process that enriches redirtraffic data with IP lists configured in RedELK (via ES app or in configuration files). *Better keep it enabled.* |
| redelk_enrich.enrich_iplists.enabled | bool | `true` | Wether to enable the enrichment module |
| redelk_enrich.enrich_iplists.interval | int | `330` | Interval (in seconds) at which the enrichment script will run |
| redelk_enrich.enrich_stage1 | object | cf. below | Enriches rtops data from Outflank's custom C2 framework. |
| redelk_enrich.enrich_stage1.enabled | bool | `false` | Wether to enable the enrichment module |
| redelk_enrich.enrich_stage1.interval | int | `300` | Interval (in seconds) at which the enrichment script will run |
| redelk_enrich.enrich_synciplists | object | cf. below | Background RedELK process that syncs IP lists from configuration files with ES. *Better keep it enabled.* |
| redelk_enrich.enrich_synciplists.enabled | bool | `true` | Wether to enable the enrichment module |
| redelk_enrich.enrich_synciplists.interval | int | `360` | Interval (in seconds) at which the enrichment script will run |
| redelk_enrich.enrich_tor | object | cf. below | Enriches redirtraffic with Tor. If an IP address is a known Tor exit node, this info is added. |
| redelk_enrich.enrich_tor.cache | int | `360` | How often the TOR endpoint list should be retrieved (in seconds). |
| redelk_enrich.enrich_tor.enabled | bool | `true` | Wether to enable the enrichment module |
| redelk_enrich.enrich_tor.interval | int | `360` | Interval (in seconds) at which the enrichment script will run |
| redelk_install_type | string | `"full"` | (`full` or `limited`) If `full`, Jupyter notebooks and BloodHound/Neo4J will be installed as well |
| redelk_loglevel | string | `"WARNING"` | Log level of the RedELK daemon. |
| redelk_notifications | object | cf. below | Alarm notifications options |
| redelk_notifications.email.enabled | bool | `false` | Wether to enable alarm notifications via e-mail |
| redelk_notifications.email.from | string | `"redelk@example.com"` | Source e-mail address to send RedELK notifications from |
| redelk_notifications.email.smtp.host | string | `"example.com"` | SMTP server hostname or IP address |
| redelk_notifications.email.smtp.login | string | `"redelk@example.com"` | SMTP username to authenticate |
| redelk_notifications.email.smtp.pass | string | `"redelk"` | SMTP password to authenticate |
| redelk_notifications.email.smtp.port | string | `"587"` | SMTP server port |
| redelk_notifications.email.to | list | `["redelk@example.com"]` | List of e-mail addresses to send RedELK notifications to |
| redelk_notifications.msteams.enabled | bool | `false` | Wether to enable alarm notifications via Microsoft Teams WebHook |
| redelk_notifications.msteams.webhook_url | string | `""` | Microsoft Teams WebHook URL |
| redelk_notifications.slack.enabled | bool | `false` | Wether to enable alarm notifications via Slack WebHook |
| redelk_notifications.slack.webhook_url | string | `""` | Slack WebHook URL |
| redelk_repo | string | `"outflanknl"` | RedELK docker image repository |
| redelk_repo_path | string | `"RedELK"` | Local path to the RedELK git repository. will be cloned if doesn't exist |
| redelk_user | string | `"redelk"` | RedELK SSH username (used to sync data between RedELK monitoring server and the clients) |
| redelk_version | string | `"master"` | RedELK version to install (ignored if the git repository defined in `redelk_repo_path` is already cloned) |
| redteam_ips | list | `[]` | List of Red Team's IP addresses |
| ssh_keys_path | string | `"ssh_keys"` | Local path to store ssh keys |
| tls_nginx_ca_path | string | `"/etc/nginx/ca_certs/ca.crt"` | Path to the CA file in Nginx container |
| tls_nginx_crt_path | string | `"/etc/letsencrypt/live/{{ external_domain }}/fullchain.pem"` | Path to the certificate file in Nginx container |
| tls_nginx_key_path | string | `"/etc/letsencrypt/live/{{ external_domain }}/privkey.pem"` | Path to the private key file in Nginx container |
| unknown_ips | list | `[]` | List of Unknown IP addresses |

## Dependencies

There is no specific dependency for this module.

## Example Playbook

```yaml
- name: Gather facts from all hosts
  hosts: all
  gather_facts: True

- name: Apply redelk-server role to monitoring server(s)
  hosts: monitoring
  gather_facts: True
  tags:
    - monitoring
  roles:
    - redelk-server
```

## Example inventory

```
[monitoring]
redelk-server  ansible_user=rtoperator  ansible_host=192.168.20.150  ansible_become_password=redelk  type=monitoring

[teamservers]
c2-01          ansible_user=rtoperator  ansible_host=192.168.20.151  ansible_become_password=redelk  type=c2

[redirectors]
redir-01       ansible_user=rtoperator  ansible_host=192.168.20.152  ansible_become_password=redelk  type=redirector
```

## Source Code

* <https://github.com/fastlorenzo/redelk-server>

## License

BSD 3-Clause

## Maintainers

Lorenzo Bernardi / [@fastlorenzo](https://twitter.com/fastlorenzo)
