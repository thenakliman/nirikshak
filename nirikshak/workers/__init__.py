import logging
import pkgutil

LOG = logging.getLogger(__name__)

print(__path__)
# fixme(thenakliman): Fix such that workers are loaded
# Automatically.
def load_workers():
    for loader, name, _ in pkgutil.walk_packages(__path__):
        try:
            loader.find_module(name).load_module(name)
        except Exception:
            LOG.error("Error in loading %s worker", name, exc_info=True)
        else:
            LOG.info("%s worker loaded", name)
