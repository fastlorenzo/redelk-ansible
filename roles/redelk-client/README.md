Role Name
=========

Ansible role to deploy [RedELK](https://github.com/outflanknl/RedELK/) client components.

Requirements
------------

There is no specific requirement for this module.

Role Variables
--------------

The following variables can be modified:

| Variable | Description | Default value |
|----------|-------------|---------------|
| `es_version` | Elastic version | `7.9.2` |
| `optsec_dir` | Base directory for components install (where customer data will be stored) - allows to store on an encrypted partition/disk | `/opt` |
| `redelk_user` | RedELK SSH username (used to sync data between RedELK monitoring server and the clients) | `redelk` |
| `deploy_all_beats` | Set to true to deploy metricbeat, packetbeat and auditbeat as well | `false` |
| `ssh_keys_path` | Local path to store ssh keys | `ssh_keys` |
| `attack_scenario` | Name of the red team attack scenario. Currently only one name is supported | `red team` |

Dependencies
------------

There is no specific dependency for this module.

Example Playbook
----------------

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

License
-------

LGPLv3

Author Information
------------------

Lorenzo Bernardi / [@fastlorenzo](https://twitter.com/fastlorenzo)
