from restapp.controller_NetworkManager import NetworkManager
from netmiko import ConnectHandler


class NxOS_PortSwitch(NetworkManager):
    """ NxOS_PortSwitch:
    Manage configuration and operational status information of network nodes :
        - CREATE : Add a new configuration of a network node (initialisation)
        - READ : Query the configuration or operational status of a network node
        - UPDATE : Change the configuration of a network node
        - DELETE : Remove some piece of configuration on a network node (dismantling)
    """

    def __init__(self, ParentsDict):
        """ NxOS_PortSwitch constructor:
        - Parents : dictionary of all parents resources
        """
        super(NxOS_PortSwitch, self).__init__(ParentsDict)
        self.Switch = self.Parents['Switches']


    def create(self, element):
        """ add a new piece of configuration (initialisation)"""
        InterfaceName = element.Name
        InterfaceSpeed = element.Speed
        InterfaceDuplex = element.Duplex
        InterfaceAdmStatus = element.Status


        # Manage NxOS connection
        platform = 'cisco_nxos'
        host = self.Switch.ManagementIP
        username = 'admin'
        password = 'admin'

        # do the change here
        device = ConnectHandler(device_type=platform, ip=host, username=username, password=password)
        device.config_mode()
        config_commands = []
        config_commands.append('interface ' + InterfaceName)
        config_commands.append('speed ' + InterfaceSpeed)
        config_commands.append('duplex ' + InterfaceDuplex)
        if InterfaceAdmStatus == 'enable':
            config_commands.append('no shutdown')
        elif InterfaceAdmStatus == 'disable':
            config_commands.append('shutdown')
        config_commands.append('switchport')
        config_commands.append('switchport mode access')
        config_commands.append('switchport access vlan 1000')
        config_commands.append('description test automation')
        output = device.send_config_set(config_commands)
        device.exit_config_mode()
        device.disconnect()
        return True


    def read(self, **kwargs):
        """ read the real configuration if needed """
        # Nothing to do for the moment ...
        return True


    def update(self, **kwargs):
        """ change a piece of configuration (update of an existing config)"""
        # Nothing to do for the moment ...
        return False


    def delete(self, **kwargs):
        """ remove a piece of configuration (desactivation of an existing configuration)"""
        # Nothing to do for the moment ...
        return False