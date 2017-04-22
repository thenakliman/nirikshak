*******************
Processing Pipeline
*******************

This section describes processing pipeline, how data will be processed through
different modules available in this software. It shows data flow among modules.
Following are the components of Nirikshak
1. Input Module(IM)
2. Controller Module(CM)
3. Processing Module(PM)
4. Post Processing Module(PPM)
5. Output Module(OM)

Data flow among them::

                                           +-----+
                                           | CLI |
               +-----------------+         +-----+         +------------+
               | Post Processing |            | 1          | Input      |
               | Module(PPM      |  5         V         2  | Module(IM) |
               +-----------------+<---->+------------+<--->+------------+
                                        | Controller |     
                                    4   | Module(CM) | 3
                    +------------+<---->+------------+<--->+------------+
                    | Processing |            |            | Processing |
                    | Module(PM) |            | 6          | Module(PM) |
                    +------------+            v            +------------+
                                        +------------+  
                                        | Output     | 
                                        | Module(OM) | 
                                        +------------+ 
                                        

#. Currently niriskshak is operated through command line, but in future it can
   be made to run continuosly then it's role will be changed from verifier to
   monitor and notifier.

#. CLI prvided will be **nirikshak**::

      nisikshak [--tags=tag1,tag2]  [--xxxxx=abc,cde]

#. CLI invokes the controller to performs its task, it passes tags and xxxxx
   along the call. Not controller(CM) decides, how input will be taken.
   Currently multiple input mechanism will be supported to provide fetch data
   for example, file, through REST call or database.

   Currently only file will be used for input but later on, if it is made
   daemon then we might think of adding database and REST APIs.

   The motivation for adding are, in distributed system many things changes
   from time to time to update large file's will be difficult to update with
   hand therefore those files can be exposed over the REST APIs and nirikshak
   call the APIs
   to get latest data.

   In case someone does not want to expose configuration over network due to
   security reason then to cope with the problem configurations are stored in
   databases and cli will provide interface to update, add and delete
   configurations easily. Databases can have multiple types for example, file
   based, mysql, in memory key value store(consul, redis) etc.

#. Controller decides input method through configuration in default group and
   **input_method** parameter. Its value currently supported is file only.

#. Controller checks parameter value from the configuration file(default file)
   and based on check following corresponding file's main method is called
   with key value parameters received from the command line arguments::

     nirikshak
       |__ input
            |__file
            |    |__main()
            |
            |__mysql
            |    |__main()
            |
            |__rest 
                 |__main()

   Make sure name for input_method configuration is correct otherwise, it will
   not be able to fine method. And main recevies key value arguments only.

#. Depending on the method used for storing configuration file's, information
   returned from all the method is the same, list of xxxxx and list of groups
   to be executed and their configuration file in json format.

#. Once above mentioned information is recevied from the input module then
   controller decides the groups to be executed and corresponding verification
   to be done from the stored jaanch.

#. Question is how does nirikshak identifies, who(module) will performs
   verification. Each of the jaanch contains mandatory field **type**. Well input
   can be defined in following formats

     1. category/plugin
     2. plugin

   In first case categories are network, disk etc. and plugin are like
   disk_usage, ip, bonds etc.

   If user provides category as well then it becomes easy for the locating the
   plugin. Location of the processing module will be::

     plugin:
        |___network
        |       |____network_ip
        |       |____network_bond
        |       |____network_team
        |
        |___disk
        |      |___disk_usage
        |      |___disk_free
        |      |___disk_list
        |
        |___process/service
               |___process_running
               |___process_enabled

   Above list is an example and incomplete. More of these can be added
   on demand.

   Whenever a user specifies network/network_ip then finding processing module
   is easy. Goto network package -> Goto network_ip file --> call main method.
   argument's are key value pair other's are not accepted.


   Now the case, when user specifies only network_ip then nirikshak searches
   recursively in plugins directory, it is costly but provides flexibility.

   Once we have the module, we can load it and run the main method defined in
   it. It accepts the complete configuration defined in the jaanch and perform
   operations, finally put the result with received configuration updated with
   result.

#. CM creates process for each of the group. All the created process shares the
   results of jaanch through queue and controller process reads the information
   from the queue and sends the received result for preprocess to pre
   processing module(PPM).

   CM keeps on waiting for the items in the queue, on getting new item in the
   queue, it send it for post processing module.

#. What pre post processing module has to be called depends on the
   configuration for that particular jaanch, and up in
   hierarchy(mentioned later)::
       nirikshak
            |____posttask
                     |_____boolean
                     |_____json
   
   With this hierarchy, we know where to search for a module, go directly to
   nirikshak/posttask and search for the module, whose names are defined in
   the configuration files. And as usually call it's main method with key
   value arguments. Post task does the required operations on the data
   recevied. Operation might involve deleting un necessary configurations
   recevied from the input or converting result to json etc.

#. Controller based on the output method defined in the configuration file
   calls the corresponding method. Methods to search for is looked into
   the output directory::

     niriskshak
          |_____output
                  |_____file
                  |_____network
                  |_____webserver

#. Controller dies, when all of its child process are died. Timeout option
   is not thought, yet. But it is good feature to provide in the feature.
