from flask import jsonify
from flask import abort
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor
from collections import namedtuple
from ansible.plugins.callback import CallbackBase
import os

class ResultCallback(CallbackBase):
    """CallBack class which is managing results display"""
    def __init__(self):
        super(ResultCallback, self).__init__()
        # store all results
        self.results = []

    def v2_runner_on_ok(self, result, **kwargs):
        """values to be displayed when playbook excution is OK"""
        host = result._host
        task = result._task

        output = result._result
        if result._result.get('changed', False):
            status = 'changed'
        else:
            status = 'ok'
        self.results.append({"host": host.name, "action":task.action, "status":status, "output": output})

    def v2_runner_on_failed(self, result, ignore_errors=False):
        delegated_vars = result._result.get('_ansible_delegated_vars', None)
        host = result._host
        task = result._task
        output = result._result
        status = 'failed'
        self.results.append({"host": host.name, "action":task.action, "status":status, "output": output})

    def v2_runner_on_skipped(self, result):
        host = result._host
        task = result._task
        output = ''
        status = 'skipped'
        self.results.append({"host": host.name, "action":task.action, "status":status, "output": output})


    def v2_runner_on_unreachable(self, result):
        host = result._host
        task = result._task
        output = ''
        status = 'unreachable'
        self.results.append({"host": host.name, "action":task.action, "status":status, "output": output})

    def v2_runner_on_no_hosts(self, task):
        host = 'no host matched'
        task = task
        output = ''
        status = 'skipped'
        self.results.append({"host": "no host matched", "action":task, "status":"skipped", "output": output})


def ansible-playbook-run():
    """ run an Ansible Playbook"""

    # Playbook execution variables setup
    Options = namedtuple('Options',
                         ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks',
                          'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                          'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])
    options = Options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='local',
                      module_path=None, forks=100, remote_user='slotlocker', private_key_file=None,
                      ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=None,
                      become_method=None, become_user=None, verbosity=None, check=False)

    variable_manager = VariableManager()
    variable_manager.extra_vars = {'ansible_user': 'ansible', 'ansible_port': '5986', 'ansible_connection': 'local',
                                   'ansible_password': 'pass'}  # Here are the variables used in the playbook
    loader = DataLoader()
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='fullpath/to/hosts')

    passwords = {}

    # stdout message processing
    results_callback = ResultCallback()

    playbook_path = './<playbook-file>.yml'
    if not os.path.exists(playbook_path):
         abort(400)

    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager,
                            loader=loader, options=options, passwords=passwords)
    pbex._tqm._stdout_callback = results_callback
    results = pbex.run()
    return jsonify({'Playbook Results': [Task for Task in results_callback.results]})

