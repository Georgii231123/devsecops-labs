# Operations Runbook

## Pre-flight

1. Confirm SSH access and sudo before enabling any SSH/firewall controls.
2. Run `ansible-playbook ... --check --diff`.
3. Review package, SSH, firewall and service changes.
4. Keep a second administrative session open during remote SSH changes.

## Application troubleshooting

```bash
systemctl status demo-web
journalctl -u demo-web -n 200 --no-pager
docker compose -f /opt/demo-web/compose.yml ps
docker compose -f /opt/demo-web/compose.yml logs --tail=200
nginx -t
```

## Rollback

Application image changes should use an immutable versioned tag. Roll back by restoring the previous inventory value and rerunning the `app` tag. OS-level changes should be reverted through Ansible instead of manual drift whenever possible.
