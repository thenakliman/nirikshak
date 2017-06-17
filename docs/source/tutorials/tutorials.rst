How to Use
----------

Nirikshak has to be configured to get expected behaviour. Following are the
terms used across this document as well as throughout the project.

#. **jaanch** is a unit of task configured. For example, a sshd service status
   has to findout and ssh package version numbers is to be checked then there
   are two jaanch

   1. Knowing service status
   2. Finding package version

#. **soochi** is the collection of jaanches to be done. For exmaple, Nirikshak
   is being used as health check system as well as monitoring system. In both
   the role, it will be doing different jaanch therefor, we can combine all
   the jaanch to be done as 'monitoring' in a single soochi and all the task
   to be done during health checking in 'health_check' soochi. When a
   particular role is expected from the nirkshak then corresponding soochi is
   mentioned in the command line argument and nirikshak will perform all the
   jaanch defined in the soochi.

#. **group** is combination of soochis and other group. The purpose of group is to
   satisfy and use reuse existing soochi without modification. For example,
   some group of soochis can be executed during monitoring as well as
   health_check, put them in separate group and include it in both the group
   declaration.

**How to define a jaanch**
A jaanch can be defined in following way,

.. code::

  port_5000:
    type: network_port
    input:
      args:
        ip: 192.168.1.100
        port: 5000
    output:
      type: yaml

The detailed description of it can be found in input section.

Nirikshak has following command line execution options available

.. code::

  nirikshak [-h] [--soochis s [s ...]] [--config-file c] [--groups g [g ...]]

Where **--soochis s1 s2**, s1, s2 are the list of soochis defined and
**--groups g1 g2** are the list of groups defined in the main.yaml file.


All the configuration files, which act as work unit are placed in
**/var/nirikshak** directory and global configuration options like log
directory are available **/etc/nirikshak/nirikshak.conf**.

The main.yaml file defines list of groups, which can be passed as command
line argument. All the defined soochi in groups must be defined with the same
name of the soochi, for Example main.yaml

.. code::

  deployment:
    config:
      post_task: dummy
      input:
        type: file
      output:
        type: json
    soochis:
      keystone_check:
        soochi: keystone
      glance_check:
        soochi: glance

  monitor:
    groups:
     - deployment
    soochis:
      keystone_monitor:
        soochi: keystone
      glance_monitor:
        soochi: glance

deploymemt and monitor are the two groups defined and can be passed as command
line argument to --group option. deployment groups defines 'keystone_check' and
'glance_check' soochi. these names does not have any restriction till they
follow yaml and json naming convetion.

Now jaanches are defined in the correspnding files in the same folder, where
main.yaml is placed.

.. code::

  File Name: keystone_check.yaml  # soochi defined in group main.yaml

  jaanches: 
    port_5000:
      type: network_port
      input:
        args:
          ip: 192.168.1.100
          port: 5000
      output:
        type: yaml
    port_35357:
      type: network_port
      post_task: dummy
      input:
        args:
          ip: 192.168.1.100
          port: 35357
      output:
        type: json
    disk:
      type: disk_partition
      input:
        args:
          device: /dev/sda5
          fstype: ext4
          mountpoint: /
      output:
        type: json
    ssh:
      type: process_running
      input:
        args:
          name: sshd

Above soochi defines four jaanch, with complete description. Meaning of the
fields can be checked in the input design part.

output varies depending on the module used for the output, detailed
information will be available in output design part.

Result Json

.. code::

  {
      "disk": {
          "input": {
              "device": "/dev/sda5",
              "fstype": "ext4",
              "mountpoint": "/"
          },
          "output": {
              "actual_output": true
          }
      },
      "port_135357": {
          "input": {
              "ip": "192.168.1.100",
              "port": 35357
          },
          "output": {
              "actual_output": 11
          }
      },
  }

For other type of output modify jaanch parameter and check output.
