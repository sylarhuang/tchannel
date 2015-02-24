from __future__ import absolute_import
import socket

import pytest

from tchannel.socket import Connection
from tchannel.exceptions import InvalidMessageException


@pytest.yield_fixture
def tchannel_pair():
    """Generate a pair of connected TChannels.

    Note that the nomenclature "server" and "client" are purely for
    readability; either side can initiate a request or fulfill an RPC call.
    """
    server, client = socket.socketpair()

    server_channel = Connection(server)
    client_channel = Connection(client)
    try:
        yield server_channel, client_channel
    finally:
        client.close()
        server.close()


def test_handshake(tchannel_pair):
    """Validate the handshake exchange."""
    server, client = tchannel_pair

    client.initiate_handshake(headers={})
    server.await_handshake(headers={})


def test_handshake_pong(tchannel_pair):
    """Validate we handle invalid states."""

    server, client = tchannel_pair

    client.ping()
    with pytest.raises(InvalidMessageException):
        server.await_handshake(headers={})


def test_ping(tchannel_pair):
    """Validate the ping/pong exchange."""
    server, client = tchannel_pair

    client.ping()
    server.pong()
