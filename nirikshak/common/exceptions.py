class NirikshakException(Exception):
    msg = ("Unknown exception.")

    def __init__(self, *args, **kwargs):
        pass


class NotFoundException(NirikshakException):
    msg = "Not Found Exception."


class ConfigurationNotFound(NotFoundException):
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
