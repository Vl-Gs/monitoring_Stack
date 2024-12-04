# Ansible DockProm Monitoring Stack

This repository contains Ansible roles for deploying a comprehensive monitoring stack including Prometheus, Grafana, InfluxDB, MongoDB, and Mosquitto MQTT broker.

## Components

- **Prometheus**: Metrics collection and storage
- **Grafana**: Visualization and dashboarding
- **InfluxDB**: Time-series database
- **MongoDB**: Document database
- **Mosquitto**: MQTT message broker

## Prerequisites

- Ansible 2.9+
- Ubuntu 20.04+ target systems
- Python 3.8+
- Sudo access on target systems

## Directory Structure

```
.
├── inventories/
│   └── production/
│       ├── group_vars/
│       │   └── all.yml
│       └── hosts
├── playbooks/
│   ├── main.yml
│   └── services.yml
└── roles/
    ├── core/
    │   └── backup/
    └── services/
        ├── grafana/
        ├── influxdb/
        ├── mongodb/
        ├── mosquitto/
        └── prometheus/
```

## Features

- Automated deployment of monitoring services
- Pre-configured dashboards for all components
- Secure SSL/TLS configuration
- Automated backups
- Prometheus alerting rules
- Service monitoring and metrics collection

## Quick Start

1. Update inventory file with your target hosts:
   ```bash
   vim inventories/production/hosts
   ```

2. Configure variables in group_vars:
   ```bash
   vim inventories/production/group_vars/all.yml
   ```

3. Run the playbook:
   ```bash
   ansible-playbook -i inventories/production/hosts playbooks/main.yml
   ```

## Dashboards

Pre-configured Grafana dashboards are included for:
- System Overview
- MongoDB Monitoring
- InfluxDB Monitoring
- Mosquitto MQTT Monitoring

## Security

- All services are configured with authentication
- SSL/TLS encryption enabled by default
- Secure default configurations
- Regular security updates

## Backup

Automated backup configuration for:
- MongoDB databases
- InfluxDB data
- Configuration files
- SSL certificates

## Monitoring

- Node metrics (CPU, Memory, Disk, Network)
- Database metrics
- Message broker metrics
- Application metrics
- Custom metrics via Prometheus exporters

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Author

Your Organization Name
