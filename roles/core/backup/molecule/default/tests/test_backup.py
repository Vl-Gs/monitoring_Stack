import os
import pytest

def test_backup_directories(host):
    """Test that backup directories exist with correct permissions."""
    dirs = [
        "/var/backup",
        "/var/backup/monitoring",
        "/var/backup/databases",
        "/var/backup/configs"
    ]
    
    for d in dirs:
        dir = host.file(d)
        assert dir.exists
        assert dir.is_directory
        assert dir.mode == 0o750
        assert dir.user == "root"
        assert dir.group == "root"

def test_backup_scripts(host):
    """Test that backup scripts are installed and executable."""
    scripts = [
        "backup-monitoring.sh",
        "backup-databases.sh",
        "restore-monitoring.sh",
        "health-check.sh"
    ]
    
    for script in scripts:
        path = f"/usr/local/bin/{script}"
        file = host.file(path)
        assert file.exists
        assert file.is_file
        assert file.mode == 0o750
        assert file.user == "root"
        assert file.group == "root"

def test_systemd_services(host):
    """Test that systemd services are enabled and running."""
    services = [
        "monitoring-health.timer"
    ]
    
    for service in services:
        assert host.service(service).is_enabled
        assert host.service(service).is_running

def test_logrotate_config(host):
    """Test that logrotate configuration is correct."""
    config = host.file("/etc/logrotate.d/monitoring")
    assert config.exists
    assert config.is_file
    assert config.mode == 0o644
    assert config.user == "root"
    assert config.group == "root"
    
    # Check content
    assert config.contains("/var/log/monitoring-health.log")
    assert config.contains("/var/log/prometheus/*.log")
    assert config.contains("/var/log/grafana/*.log")
    assert config.contains("/var/log/influxdb/*.log")
    assert config.contains("/var/log/mosquitto/*.log")

def test_cron_jobs(host):
    """Test that cron jobs are configured."""
    crontab = host.run("crontab -l")
    assert crontab.rc == 0
    
    # Check for backup jobs
    assert "/usr/local/bin/backup-monitoring.sh" in crontab.stdout
    assert "/usr/local/bin/backup-databases.sh" in crontab.stdout

def test_backup_execution(host):
    """Test that backup script executes successfully."""
    cmd = host.run("/usr/local/bin/backup-monitoring.sh")
    assert cmd.rc == 0
    
    # Check for backup files
    backup_files = host.run("find /var/backup/monitoring -type f -name '*.tar.gz' -mtime -1")
    assert backup_files.rc == 0
    assert len(backup_files.stdout.strip()) > 0

def test_health_check(host):
    """Test that health check script executes successfully."""
    cmd = host.run("/usr/local/bin/health-check.sh")
    assert cmd.rc == 0
    
    # Check log file
    log = host.file("/var/log/monitoring-health.log")
    assert log.exists
    assert "Starting health check" in log.content_string
