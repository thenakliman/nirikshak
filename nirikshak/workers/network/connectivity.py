import logging
import ping

from nirikshak.workers import base
from nirikshak.common import plugins

LOG = logging.getLogger(__name__)


@plugins.register("network_connectivity")
class Connectivity(base.Worker):
    @base.match_expected_output
    @base.validate(required=("host",))
    def work(self, **kwargs):
        host = kwargs["input"]["args"]["host"]
        try:
            float(ping.Ping(host).do())
        except TypeError:
            LOG.info("Failed to connect to %s host", host)
            return False
        except Exception:
            LOG.error("Failed to connect to %s host", host, exc_info=True)
            return False

        LOG.info("Connected to %s host", host)
        return True
