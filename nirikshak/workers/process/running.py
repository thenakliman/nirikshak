import psutil


def work(**kwargs):
    k = kwargs['input']['args']
    name = k['name']
    for proc in psutil.process_iter():
        try:
            if proc.name() == name:
                kwargs['input']['result'] = True
                break
        except psutil.NoSuchProcess:
            pass
    else:
        kwargs['input']['result'] = False
    return kwargs
