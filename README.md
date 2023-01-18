# Ansible roles to deploy RedELK

This repository contains multiple Ansible playbook allowing to deploy [RedELK](https://github.com/outflanknl/RedELK/).

All credits goes to the authors and contributors of RedELK.

The roles can be found on the following repositories:

- [redelk-server](https://github.com/fastlorenzo/redelk-server)
- [redelk-client](https://github.com/fastlorenzo/redelk-client)

## Install requirements

```bash
ansible-galaxy install -r requirements.yml
ansible-galaxy collection install community.crypto
ansible-galaxy collection install community.general
```

## Deploy RedELK

```bash
ansible-playbook -i inventory install-redelk.yml -K
```

## Remove systemd-resolved stub listener (to free port 53 for DNS redirectors)

```bash
sed -i 's/#DNSStubListener=yes/DNSStubListener=no/g /etc/systemd/resolved.conf'
sudo rm /etc/resolv.conf
sudo ln -s /run/systemd/resolve/resolv.conf /etc/
sudo systemctl restart systemd-resolved.service
```
