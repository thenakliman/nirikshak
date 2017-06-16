import pkgutil


# FIXME(thenakliman): Fix such that workers are loaded
# Automatically.
def load_workers():
    for loader, name, _ in pkgutil.walk_packages(__path__):
        loader.find_module(name).load_module(name)
