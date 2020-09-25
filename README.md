```
ansible-galaxy install -r requirements.yml
ansible-galaxy collection install community.crypto
ansible-playbook -i inventory install-redelk.yml -K
```

## Remove systemd-resolved stub listener (to free port 53)

```
sed -i 's/#DNSStubListener=yes/DNSStubListener=no/g /etc/systemd/resolved.conf'
sudo rm /etc/resolv.conf
sudo ln -s /run/systemd/resolve/resolv.conf /etc/
sudo systemctl restart systemd-resolved.service
```
