from nirikshak.output import base


@base.register('console')
class ConsoleFormatOutput(base.FormatOutput):
    def output(self, **args):
        k = args.keys()[0]
        print(args[k]['formatted_output'])
