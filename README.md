# Ansible roles to deploy RedELK

This repository contains multiple Ansible roles allowing to deploy [RedELK](https://github.com/outflanknl/RedELK/).

All credits comes to the authors and contributors of RedELK.

## Install requirements

```
ansible-galaxy install -r requirements.yml
ansible-galaxy collection install community.crypto
```

## Deploy RedELK

```
ansible-playbook -i inventory install-redelk.yml -K
```

## Remove systemd-resolved stub listener (to free port 53 for DNS redirectors)

```
sed -i 's/#DNSStubListener=yes/DNSStubListener=no/g /etc/systemd/resolved.conf'
sudo rm /etc/resolv.conf
sudo ln -s /run/systemd/resolve/resolv.conf /etc/
sudo systemctl restart systemd-resolved.service
```
