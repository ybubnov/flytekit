from __future__ import absolute_import

from flytekit.clis.auth.auth import AuthorizationClient as _AuthorizationClient
from flytekit.clis.auth.discovery import DiscoveryClient as _DiscoveryClient

from flytekit.configuration.creds import (
    REDIRECT_URI as _REDIRECT_URI,
    CLIENT_ID as _CLIENT_ID
)
from flytekit.configuration.platform import URL as _URL

try:  # Python 3
    import urllib.parse as _urlparse
except ImportError:  # Python 2
    import urlparse as _urlparse

# Default, well known-URI string used for fetching JSON metadata. See https://tools.ietf.org/html/rfc8414#section-3.
discovery_endpoint_path = ".well-known/oauth-authorization-server"


def _get_discovery_endpoint():
    return _urlparse.urljoin(_URL.get(), discovery_endpoint_path)


# Lazy initialized authorization client singleton
_authorization_client = None


def get_client():
    global _authorization_client
    if _authorization_client is not None:
        return _authorization_client
    discovery_endpoint = _get_discovery_endpoint()
    discovery_client = _DiscoveryClient(discovery_url=discovery_endpoint)
    authorization_endpoints = discovery_client.get_authorization_endpoints()

    _authorization_client =\
        _AuthorizationClient(redirect_uri=_REDIRECT_URI.get(), client_id=_CLIENT_ID.get(),
                             auth_endpoint=authorization_endpoints.auth_endpoint,
                             token_endpoint=authorization_endpoints.token_endpoint)
    return _authorization_client


def get_authorization_endpoints():
    discovery_endpoint = _get_discovery_endpoint()
    discovery_client = _DiscoveryClient(discovery_url=discovery_endpoint)
    return discovery_client.get_authorization_endpoints()