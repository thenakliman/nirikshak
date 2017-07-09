Interaction
-----------

**jaanch** cli will be provided, which start the verification process.
When command is fired then main.yaml file at following location::

               **/var/nirikshak/conf/**  

is read and identifies, how many groups will require execution defined
in the main.yaml file. Then based on system processor's cores, processes
are created, which indepandently performs the task. Results from multiple
process are put into the queue and the main process consumes the data from
the queue. There will be flag in the callable, which controls that data
has to be written as response is received in the queue or all at once.

Interation among different module is going to be following::


                      +---------+             
                      | jaanch  |             
                      +---------+             
                           |                          
                           v                          
                 +----------------------+     
                 | Read main.yaml and   |     
                 | find number of soochi |     
                 +----------------------+     
                           |
                           |
                           |
                           v
                    +-------------+                                                      |  |
     +--------+     |             |           +------------------+                       |  |
     | Output |<----|   Perform   |           |  Preprocessing   |                       |  |
     +--------+     |   Jaanch    |<--------->|    task          |                       |  |
                    |             |           +------------------+                       |  |
                    |             |<-----------------------------------------------------|  |
                    +-------------+                                                      |  |
                          |                                                              |  |
                          | dispatch processes                                           |  |
                          V                                                              |  |
  ----------------------------------------------------------------------------+          |  |
         |                 |                    |                             |          |  |
  +-------------+   +-------------+      +-------------+               +-------------+   |  |
  |             |   |             |      |             |               |             |   |  |
  |   Perform   |   |  Perform    |      |    Perform  |               |  Perform    |   |__|
  |   Jaanch    |   |  Jaanch     |      |    Jaanch   |  -  -  -  -   |  Jaanch     |   |r5|
  |             |   |             |      |             |               |             |   |__|
  |             |   |             |      |             |               |             |   |r4|
  +-------------+   +-------------+      +-------------+               +-------------+   |__|
         |  p1             |    p2              |    p3                      |      pn   |r3|
         |                 |                    |                            |           |__| 
         |                 |                    |                            |           |r2| 
         V                 V                    V                            V           |__| 
  -------------------------------------------------------------------------------------->|r1| 
                                                                                         +--+
