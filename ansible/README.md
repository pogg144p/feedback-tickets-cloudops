# Automated EC2 Server Configuration with Ansible

This directory contains production-grade Ansible playbooks, roles, and inventory configurations designed to automate the provisioning, security hardening, and software deployment across AWS EC2 instances (Ubuntu 22.04 LTS).

Developed based on infrastructure patterns utilized during the **Tata STRIVE** cloud administration workflows, replacing manual server configuration with declarative, idempotent Infrastructure as Code (IaC).

---

## 🏗️ Architecture & Roles

The orchestration is structured into modular roles under `ansible/roles/`:

```
ansible/
├── ansible.cfg                    # Default connection, timeout & privilege escalation settings
├── inventory/
│   └── hosts.ini                  # Grouped server inventory (webservers, appservers)
├── playbooks/
│   └── site.yml                   # Master execution playbook
└── roles/
    ├── server_common/             # Baseline hardening & utilities
    │   └── tasks/main.yml         # Apt updates, fail2ban, UFW firewall, deployer user with sudo
    ├── docker_engine/             # Container runtime deployment
    │   └── tasks/main.yml         # Official Docker CE repo, GPG keyrings, docker-compose plugin
    └── web_proxy/                 # Web ingress & load distribution
        ├── defaults/main.yml      # Configurable proxy host, port, domain variables
        ├── templates/app.conf.j2  # Jinja2 NGINX reverse proxy template with health checks
        ├── handlers/main.yml      # Safe systemd reload handlers
        └── tasks/main.yml         # Site activation, symbolic links, HTTP/HTTPS firewall
```

---

## 🚀 Execution Guide

### 1. Dry Run / Syntax Validation (Check Mode)
Before making changes on remote instances, perform a syntax check and dry run to verify idempotency:

```bash
# Check syntax
ansible-playbook -i inventory/hosts.ini playbooks/site.yml --syntax-check

# Dry-run execution without modifying state
ansible-playbook -i inventory/hosts.ini playbooks/site.yml --check
```

### 2. Live Execution
Execute against the targeted hosts using SSH key authentication:

```bash
ansible-playbook -i inventory/hosts.ini playbooks/site.yml
```

### 3. Targeted Role Execution (Tags / Limits)
To provision only web servers or apply security updates without touching application nodes:

```bash
# Target only the webservers group
ansible-playbook -i inventory/hosts.ini playbooks/site.yml --limit webservers

# Run specific tasks or roles
ansible-playbook -i inventory/hosts.ini playbooks/site.yml -t docker
```

---

## 💼 ATS Keywords & Interview Talking Points

### Resume Bullet Point:
> *"Automated end-to-end AWS EC2 instance provisioning and OS hardening using modular Ansible roles; standardized Docker container runtimes, NGINX reverse proxy configurations, and UFW firewall security with 100% idempotent playbooks."*

### Key Concepts to Mention in Interviews:
- **Idempotency:** Running the playbook 1 time or 100 times yields the exact same state without unintended side-effects.
- **Handlers:** NGINX is only reloaded if the Jinja2 template actually changed, preventing unnecessary service restarts.
- **Principle of Least Privilege:** SSH hardening, dedicated `deployer` service user with controlled sudo permissions instead of relying on root credentials.
- **Separation of Concerns:** Distinct roles (`server_common`, `docker_engine`, `web_proxy`) allow independent updates and testing.
