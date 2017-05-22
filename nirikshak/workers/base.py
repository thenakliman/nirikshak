import logging

from nirikshak.common import exceptions


def validate(required=(), optional=()):
    def func(f):
        def validator(**kwargs):
            require = set(required)
            try:
                available = set(kwargs['input']['args'].keys())
            except KeyError:
                available = set()

            missing = require - available
            if missing:
                raise excpetions.MissingRquiredArgException(jaanch=missing)

            require.update(set(optional))
            extra = available - require
            if extra:
                raise exceptions.ExtraArgException(params=[list(extra)])

            return f(**kwargs)
        return validator
    return func


def match_expected_output(validator):
    def convert_output(**kwargs):
        tmp = validator(**kwargs)
        if 'result' in kwargs['output']:
            tmp = (tmp == kwargs['output']['result'])

        kwargs['input']['result'] = tmp
        return kwargs

    return convert_output
