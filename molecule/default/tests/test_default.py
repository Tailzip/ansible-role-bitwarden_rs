import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_openssl_package(host):
    package = host.package('openssl')

    assert package.is_installed


def test_user(host):
    user = host.user('bitwarden')

    assert user.exists
    assert user.name == 'bitwarden'
    assert user.group == 'bitwarden'
    assert user.shell == '/sbin/nologin'
    assert not host.file('/home/bitwarden').exists


def test_log_file(host):
    log_file = host.file('/var/log/bitwarden.log')

    assert log_file.exists
    assert log_file.user == 'bitwarden'
    assert log_file.group == 'root'
    assert log_file.mode == 0o640


def test_binary_file(host):
    binary_file = host.file('/usr/bin/bitwarden')

    assert binary_file.exists
    assert binary_file.user == 'bitwarden'
    assert binary_file.group == 'root'
    assert binary_file.mode == 0o750


def test_config_file(host):
    config_file = host.file('/etc/bitwarden/bitwarden.env')

    assert config_file.exists
    assert config_file.user == 'bitwarden'
    assert config_file.group == 'bitwarden'
    assert config_file.mode == 0o640


def test_web_vault_files(host):
    web_vault_dir = host.file('/var/lib/bitwarden/web-vault')
    index_html_file = host.file('/var/lib/bitwarden/web-vault/index.html')

    assert web_vault_dir.exists
    assert web_vault_dir.is_directory
    assert web_vault_dir.user == 'bitwarden'
    assert web_vault_dir.group == 'bitwarden'
    assert web_vault_dir.mode == 0o751

    assert index_html_file.exists
    assert index_html_file.user == 'bitwarden'
    assert index_html_file.group == 'bitwarden'
    assert index_html_file.mode == 0o550


def test_service(host):
    service = host.service('bitwarden')

    assert service.is_running
    assert service.is_enabled
