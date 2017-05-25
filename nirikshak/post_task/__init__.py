import pkgutil


for loader, name, _ in pkgutil.walk_packages(__path__):
    loader.find_module(name).load_module(name)
