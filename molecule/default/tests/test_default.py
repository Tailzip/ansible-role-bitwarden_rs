import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_user(host):
    user = host.user('bitwarden')

    assert user.exists
    assert user.name == 'bitwarden'
    assert user.group == 'bitwarden'
    assert user.shell == '/sbin/nologin'
    assert not host.file('/home/bitwarden').exists

def test_service(host):
    service = host.service('bitwarden')

    # assert service.is_running
    assert service.is_enabled
