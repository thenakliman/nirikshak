import apt

from nirikshak.workers import base


@base.match_expected_output
@base.validate(('package',), tuple())
def work(**kwargs):
    k = kwargs['input']['args']
    cache = apt.cache.Cache()
    cache.update()
    pkg = cache[k['package']]
    return pkg.is_installed
