"""
connector.py — Opens a PyEZ Device session to a Juniper router.
"""

from jnpr.junos import Device
from jnpr.junos.exception import ConnectError, ConnectAuthError, ConnectTimeoutError, RpcError

import config


def get_device(host: str, port: int) -> Device | None:
    """
    Opens and returns an authenticated PyEZ Device session.
    Returns None if the connection fails so the caller can skip
    unreachable routers without crashing the whole program.
    """
    try:
        dev = Device(host=host, user=config.USERNAME, passwd=config.PASSWORD, port=port)
        dev.open()
        return dev
    except ConnectAuthError:
        print(f"  [AUTH ERROR]    {host} — bad username or password")
    except ConnectTimeoutError:
        print(f"  [TIMEOUT]       {host} — router did not respond")
    except ConnectError as e:
        print(f"  [CONNECT ERROR] {host} — {e}")
    except RpcError as e:
        print(f"  [RPC ERROR]     {host} - {e}")
    except Exception as e:
        print(f"  [ERROR]         {host} - {e}")

    return None