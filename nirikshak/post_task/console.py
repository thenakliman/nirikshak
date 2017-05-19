def format_it(**args):
    name = args.keys()[0]
    v = args[name]
    inpt = ''
    for key, value in v['input']['args'].items():
        inpt = ("%s%s:%s," % (inpt, key, value))

    type_ = v['type']

    result = ''
    if 'result' in args:
        if str(v['args']['result']) == str(args['result']):
            result = 'pass'
        else:
            result = 'fail'

    if not result:
        result = v['input']['result']

    rs = ("%s,%s,%s" % (name, type_, inpt))
    rs = ("%s%s%s" % (rs, (120 - len(rs)) * '.', result))
    args[name]['formatted_output'] = rs
    return args
