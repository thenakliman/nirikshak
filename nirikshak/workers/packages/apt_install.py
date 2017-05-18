import apt


def work(**kwargs):
    k = kwargs['input']['args']
    cache = apt.cache.Cache()
    cache.update()
    pkg = cache[k['package']]
    kwargs['input']['result'] = pkg.is_installed
    return kwargs
