from flask import jsonify
from flask import abort
from restapp import app
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.parsing.dataloader import DataLoader
from ansible.executor.playbook_executor import PlaybookExecutor
from collections import namedtuple
from ansible.plugins.callback import CallbackBase
import os

#########################
# Manage Ansible STDOUT #
#########################

class ResultCallback(CallbackBase):
    """Classe CallBack qui memorise les resultats"""
    def __init__(self):
        super(ResultCallback, self).__init__()
        # store all results
        self.results = []

    def v2_runner_on_ok(self, result, **kwargs):
        """memorise le resultat quand cela se passe bien"""
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


############################################
# Manage Ansible Call from our REST Server #
############################################

@app.route('/todo/api/v1.0/ansible', methods=['GET'])
def ansible():
    """ reroute to Ansible application"""

    # Initialisation des variables
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

    # Procedure de traitement des messages de sortie
    results_callback = ResultCallback()

    # Creation de l'inventaire et transmission au "var manager"
    #inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='filename')
    inventory = Inventory(loader=loader, variable_manager=variable_manager)
    variable_manager.set_inventory(inventory)


    # Creation d'un playbook qui fait un ls puis un hello sur localhost
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
            #stdout_callback='default', # envoie les donnees sur la sortie standard
            stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin
        )
        result = tqm.run(play)
    finally:
        if tqm is not None:
            tqm.cleanup()

    return jsonify({'Playbook Results': [Task for Task in results_callback.results]})


@app.route('/todo/api/v1.0/ansible2', methods=['GET'])
def ansible2():
    """ reroute to Ansible application"""

    # Initialisation des variables
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

    # Procedure de traitement des messages de sortie
    results_callback = ResultCallback()

    playbook_path = './test.yml'
    if not os.path.exists(playbook_path):
         abort(400)

    pbex = PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=variable_manager,
                            loader=loader, options=options, passwords=passwords)
    pbex._tqm._stdout_callback = results_callback
    results = pbex.run()
    return jsonify({'Playbook Results': [Task for Task in results_callback.results]})