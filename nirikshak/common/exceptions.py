# Copyright 2017 <thenakliman@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import logging


class NirikshakException(Exception):
    msg = ("Unknown exception.")

    def __init__(self, *args, **kwargs):
        logging.error(self.message % kwargs)


class NotFoundException(NirikshakException):
    msg = "Not Found Exception."


class SectionNotFoundException(NotFoundException):
    msg = "%(section)s could not be found"


class ConfigurationNotFoundException(NotFoundException):
    msg = ("%(option)s configuration option in %(section)s section of "
           " configuration file not found.")


class FileNotFound(NotFoundException):
    msg = ("%(loction)s file not found.")


class GroupNotFoundException(NotFoundException):
    msg = ("%(req_group)s is not found, but specified in definition.")


class InvalidException(NirikshakException):
    msg = "Invalid data/input/resource/format"


class MissingRequiredArgsException(InvalidException):
    msg = "%s required arguments are missing"


class ExtraArgsException(InvalidException):
    msg = "%s extra arguments are provided"


class InvalidFormatException(InvalidException):
    msg = ("%(location)s file is not in %(format)s format.")


class InvalidInputType(InvalidException):
    msg = "Invalid %(input_type)s input type."


class InputExecutionException(NirikshakException):
    msg = "Error in execution of %(input)s input module."


class OutputExecutionException(NirikshakException):
    msg = "Error in execution of %(output)s input module."


class PostTaskException(NirikshakException):
    msg = "Error in execution of post task module."
