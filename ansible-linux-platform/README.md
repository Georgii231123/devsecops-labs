# Ansible Linux Platform Automation

A DevOps automation project for turning a fresh Ubuntu host into a repeatable application node. It separates base OS configuration, Docker runtime, reverse proxy and application deployment into reusable Ansible roles.

## What it automates

- base packages and time synchronization;
- journald retention settings;
- optional SSH hardening via drop-in configuration;
- optional UFW policy with an explicit safety switch;
- Docker Engine installation and service management;
- Nginx reverse proxy configuration;
- application directory, Docker Compose deployment and systemd lifecycle;
- environment-specific inventory and variables;
- Ansible linting and syntax validation in CI.

## Structure

```text
ansible-linux-platform/
├── inventories/dev/
├── roles/base/
├── roles/docker/
├── roles/nginx/
├── roles/app/
├── site.yml
├── requirements.yml
└── ansible.cfg
```

## Dry run first

```bash
ansible-galaxy collection install -r requirements.yml
ansible-playbook -i inventories/dev/hosts.yml site.yml --check --diff
```

Only after reviewing the diff should you run:

```bash
ansible-playbook -i inventories/dev/hosts.yml site.yml
```

`firewall_enabled` and `ssh_hardening_enabled` are disabled in the example inventory so a learner cannot accidentally lock themselves out by blindly applying the playbook.

## Interview explanation

> I split host configuration into roles so the same baseline can be reused across environments. Potentially disruptive controls such as SSH and firewall changes are feature-gated, and I expect a check-mode run before apply. The application is managed through systemd while Docker Compose describes the workload, so the node has predictable startup and restart behavior.
