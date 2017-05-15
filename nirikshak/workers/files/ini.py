import ConfigParser


def work(**kwargs):
    k = kwargs['input']['args']
    config = ConfigParser.ConfigParser()
    config.read(k['file'])
    kwargs['input']['result'] = (config.get(k['section'],
                                            k['key']) == k['value'])
    return kwargs
