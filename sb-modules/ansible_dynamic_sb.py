from flask import jsonify
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.parsing.dataloader import DataLoader
from collections import namedtuple
from ansible.plugins.callback import CallbackBase


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



def ansible-dynamic-play():
    """ run a dynamic Ansible Playbook"""

    # Playbook execution variables setup
    Options = namedtuple('Options',
                         ['connection', 'module_path', 'forks', 'remote_user', 'private_key_file', 'ssh_common_args',
                          'ssh_extra_args', 'sftp_extra_args', 'scp_extra_args', 'become', 'become_method',
                          'become_user', 'verbosity', 'check'])
    options = Options(connection='local', module_path='/path/to/mymodules', forks=100, remote_user=None,
                      private_key_file=None, ssh_common_args=None, ssh_extra_args=None, sftp_extra_args=None,
                      scp_extra_args=None, become=None, become_method=None, become_user=None, verbosity=None,
                      check=False)
    variable_manager = VariableManager()
    loader = DataLoader()
    passwords = dict(vault_pass='secret')

    # stdout message processing
    results_callback = ResultCallback()

    # Inventory Dynamic creation
    #inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='filename')
    inventory = Inventory(loader=loader, variable_manager=variable_manager)
    variable_manager.set_inventory(inventory)


    # Playbook dynamic creation (3 tasks : ls and 2 debug messages)
    play_source = dict(
        name="Ansible Play",
        hosts='localhost',
        gather_facts='no',
        tasks=[
            dict(action=dict(module='shell', args='ls'), register='shell_out'),
            dict(action=dict(module='debug', args=dict(msg='{{shell_out.stdout}}'))),
            dict(action=dict(module='debug', args=dict(msg='Hello Galaxy!')))
        ]
    )
    play = Play().load(play_source, variable_manager=variable_manager, loader=loader)

    # Excecution
    tqm = None
    try:
        tqm = TaskQueueManager(
            inventory=inventory,
            variable_manager=variable_manager,
            loader=loader,
            options=options,
            #passwords=passwords,
            passwords=None,
            #stdout_callback='default', # display data on default STDOUT
            stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
        )
        result = tqm.run(play)
    finally:
        if tqm is not None:
            tqm.cleanup()

    return jsonify({'Playbook Results': [Task for Task in results_callback.results]})