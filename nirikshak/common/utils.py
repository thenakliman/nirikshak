from copy import deepcopy


def merge_dict(dict2, dict1):
    for k, v in dict1.iteritems():
        if dict2.get(k):
            if isinstance(dict2[k], dict):
                merge_dict(dict2[k], dict1[k])
        else:
            dict2[k] = deepcopy(v)
