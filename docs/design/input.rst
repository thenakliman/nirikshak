Input
=====

This section describes design of the input, provided to the Nirikshak. To
make maintenance easier for the users, input can be provided into serveral
yaml files. There must be a main.yaml file in input folder, which describes
the input files to be processed for a particular execution. This file also
provides way of configuring the Nirikshak.

Jaanch
======

Jaanch is the verification to be done, these are defined in yaml file. We
need to define inputs and the way Jaanch has to be done. To represent Jaanch
yaml file is created for them.

If input format provides expected result then fail/pass is the output. If
input format does not provide expected result then output should be result of
verification

Jaanch's are defined in the yaml file called xxxxx, in following format::

     items: 
       # Each set of Jaanch's can be tagged with name, which can be later on
       # used for verification.
       tag: <tag name>

       # Instead of item any name can be used, but it must be
       # unique under global items of this set
       <item(name>>:

         # Each item should belong to some category, for example
         # process, network etc there type value format is  <category>/<type>
         # type reprsent actual plugin to be used for this.
         type: <category/type>

         # An item can be tagged, so that in case if particular tags of test
         # cases are to be executed it can done
         tags: <tag name>

         # Contains input to be used for verification
         input:
           # How the input will be taken for this task, for example
           # from configuration file or output from other process etc
           type: <type name>

           # if input is taken from configuration file then args
           # will be passed to method
           args:              #optional
             <arg key>: <arg value>
             <arg key>: <arg value>
             <arg key>: <arg value>

         # Contains output method for example console, file etc
         output:
           # the way output to be displayed to user for example
           # file, stdout etc
           type: <category/value>
           # precomputation/customize callable before dumping output
           pretask: <callable name>
           # If some output is expected then mention here
           result: <expected result>

main.yaml File
==============

It defines the verification to be done, as there can be multiple input files,
this file bring them together and provide a way to configure a file with
particular settings

Format of main.yaml can be following::

  <group name>:
    name: <group name>
    <configurations key>: <configuration value>
    <item>:
      xxxxx: <name of files>/<name of group>
      <configuration name>: <configuration value>
    <item>:
      xxxxx: <name of files>/<name of group>
      <configuration name>: <configuration value>

you can define <group name> and <group name>/name is the name of the group.
This way we can define multiple groups, <name of file> represents name of the
file containing the test case, you may write name with and without format of
the file. Ofcourse format of file is yaml only.

Group of groups is also possible, but the order of groups execution is not
defined because they will be executed parallely.
