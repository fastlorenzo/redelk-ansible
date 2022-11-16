# redelk-client

Ansible role to deploy [RedELK](https://github.com/outflanknl/RedELK/) client components.

## Variables

The following variables can be modified:

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| attack_scenario | string | `"redteam"` | Name of the red team attack scenario. Currently only one name is supported |
| es_deploy_beats | list | `["filebeat"]` | Set which beats to deploy (possible values: `filebeat` / `apm-server` / `auditbeat` / `heartbeat` / `metricbeat` / `nagioscheckbeat` / `packetbeat`) |
| es_version | string | `"7.16.3"` | Elastic version |
| optsec_dir | string | `"/opt"` | Base directory for components install (where customer data will be stored) - allows to store on an encrypted partition/disk |
| redelk_cert_path | string | `"certificates/redelk"` | Local path to store RedELK certificates. This should match the value of `redelk_cert_path` in `redelk-server` role. |
| redelk_server_host | string | `"localhost"` | Hostname or IP of the RedELK server (used for filebeat destination) |
| redelk_user | string | `"redelk"` | RedELK SSH username (used to sync data between RedELK monitoring server and the clients) |
| ssh_keys_path | string | `"ssh_keys"` | Local path to store ssh keys |

## Dependencies

There is no specific dependency for this module.

## Example Playbook

```yaml
- name: Apply redelk-client role to teamservers
  hosts: teamservers
  gather_facts: True
  tags:
    - teamservers
  roles:
    - redelk-client

- name: Apply redelk-client role to redirectors
  hosts: redirectors
  gather_facts: True
  tags:
    - redirectors
  roles:
    - redelk-client
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

* <https://github.com/fastlorenzo/redelk-client>

## License

BSD 3-Clause

## Maintainers

Lorenzo Bernardi / [@fastlorenzo](https://twitter.com/fastlorenzo)
