Role Name
=========

Ansible role to deploy [RedELK](https://github.com/outflanknl/RedELK/) server components.

Requirements
------------

There is no specific requirement for this module.

Role Variables
--------------

The following variables can be modified:

| Variable | Description | Default value |
|----------|-------------|---------------|
| `es_version` | Elastic version | `7.9.2` |
| `es_heap_size` | ElasticSearch memory size | `1g` |
| `es_elastic_password` | ElasticSearch users | `elastic` |
| `es_logstash_system_password` | ElasticSearch `logstash_system` user's password | `logstash_system` |
| `es_kibana_password` | ElasticSearch `kibana` user's password | `kibana` |
| `es_redelk_user` | ElasticSearch RedELK username | `redelk` |
| `es_redelk_password` | ElasticSearch RedELK user's password | `redelk` |
| `es_kibana_encryptionKey` | Kibana encryption key (32 char alphanumeric) | `sLOVUK5MLv0VDhKsMlQcjgAaSMLXLLVy` |
| `optsec_dir` | Base directory for components install (where customer data will be stored) - allows to store on an encrypted partition/disk | `/opt` |
| `redelk_user` | RedELK SSH username (used to sync data between RedELK monitoring server and the clients) | `redelk` |
| `ssh_keys_path` | Local path to store ssh keys | `ssh_keys` |
| `redelk_ca_password` | CA password used to generate ES certificates | `ChangeMe` |
| `redelk_cert_path` | Local path to store RedELK certificates | `certificates/redelk` |
| `redelk_alarm_Verbosity` |  | `0` |
| `redelk_alarm_interval` |  | `3600` |
| `redelk_alarm_vt_apikey` |  | `<<INSERT_API_KEY>>` |
| `redelk_alarm_ibm_BasicAuth` |  | `Basic <<REPLACE>>` |
| `redelk_alarm_HybridAnalysisAPIKEY` |  | `<<INSERT_API_KEY>>` |
| `redelk_alarm_smtpSrv` |  | `mail.bernardi.be` |
| `redelk_alarm_smtpPort` |  | `587` |
| `redelk_alarm_smtpName` |  | `redelk@bernardi.be` |
| `redelk_alarm_smtpPass` |  | `<<SMTP_PASS>>` |
| `redelk_alarm_fromAddr` |  | `redelk@bernardi.be` |
| `redelk_alarm_toAddr` |  | `redelk@bernardi.be` |
| `redelk_alarm_tempDir` |  | `/tmp` |
| `redelk_alarm_msteams_webhook_url` |  | `` |
| `customer_ips` | List of customer's IP addresses | `[]` |
| `redteam_ips` | List of Red Team's IP addresses | `[]` |
| `unknown_ips` | List of Unknown IP addresses | `[]` |
| `domains` | List of domain names used for the exercise | `[]` |

Dependencies
------------

There is no specific dependency for this module.

Example Playbook
----------------

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

License
-------

LGPLv3

Author Information
------------------

Lorenzo Bernardi / [@fastlorenzo](https://twitter.com/fastlorenzo)
