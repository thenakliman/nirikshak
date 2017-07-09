Usage
=====

Nirikshak can be used as System verifier, health check tool, monitoring tool
testing tools etc. It depends completly on you, how you configure it to behave.
All you needs to do is configuration, if pluggable modules are available. If no
module is available then you have to write your own, because nirikshak does not
know, what and how to test :).

Use Cases
---------

#. **Nirikshak** can be used as **orchestration tool**, for example a
   developer needs to create network, router, subnet, attach subnet to router
   in OpenStack cluster. You are thinking about **heat**, openstack component.
   we can achieve it without heat as well, we create module's for all these
   and orchestrate them. Why should i use nirikshak instead of heat? You are
   right, heat is their in this scenario but not available in all the
   distributed systems. It was just an example, how we can use Nirikshak.

#. You have an OpenStack setup on 1000 nodes and suddenly something went wrong
   on a nodes and all of the VMs are not accessible then you need to start
   investigation from the basic operation. Administrator has to identify
   possible reasons and then eliminate them one by one after verification.

   **How Nirikshak Helps?**

   At the time of installation you defined certain expected parameters for
   disk available size should be atleast this much etc. neutron agent must be
   running etc. and when issue occue, administrator unlease the beast, it
   identify abnormal behaviour for you.

#. Let's consider the use of a health check system, where we have to find out
   the health of the hadoop cluster. Well, hadoop cluster contains many services
   and different hardware to monitor. HA of networking, services etc, is going to
   exist in production enviorment. And checking health of the 100 nodes(cluster
   size) can be painfull. Nirikshak comes right here to resuce you from the pain.

   Well you need to identify, what is the correct health parameter of the hadoop
   cluster and how to measure those parameter, once you have the list, now turn
   that list into nirikshak configuration, its that simple.

#. A distributed cluster was installed on the thousands of nodes, now after
   installation you want to verify that installation is succesful. All the
   configuration parameters are set correctly on all the machine's. All the
   services are running on the machine. **Are you gonna do it manually?** I
   don't think so, you gonna write the script. The other team is going to do
   almost similar thing but they don't about your script or even if they do
   parameters will differ and most of them will be hardcoded. So they gonna
   write their own scripts well wastage of effort. **Nirikshak is going to
   make standard module** which can be reused with changing the configuration
   file.

Above are some of the ways, nirikshak can be configured. It is upto your
problem solving skills and imagination, which decide how you use this
framework.

.. include:: tutorials.rst
