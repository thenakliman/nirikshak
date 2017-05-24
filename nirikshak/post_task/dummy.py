from nirikshak.post_task import base


@base.register('dummy')
class FormatOutputConsole(base.FormatOutput):

    def format_output(self, **args):
        return args
