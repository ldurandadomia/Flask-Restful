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
