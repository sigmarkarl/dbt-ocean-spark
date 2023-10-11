from thrift.transport.TTransport import TTransportBase
from websockets.sync.client import connect
import Union


class TWebSocket(TTransportBase):
    """Base class for Thrift transport layer."""

    def __init__(self, url: str, token: str) -> None:
        self.url = url
        self.token = token
        self.opened = False

    def isOpen(self) -> bool:
        return self.opened

    def open(self) -> None:
        self.opened = True
        self.ws = connect(
            self.url,
            subprotocols=None,
            additional_headers={"Authorization": f"Bearer {self.token}"},
        )

    def close(self) -> None:
        self.ws.close()

    def read(self, sz: int) -> Union[bytes, str]:
        return self.ws.recv(sz)

    def readAll(self, sz: int) -> bytes:
        buff = b""
        have = 0
        while have < sz:
            chunk = self.read(sz - have)
            chunkLen = len(chunk)
            have += chunkLen
            buff += chunk

            if chunkLen == 0:
                raise EOFError()
        return buff

    def write(self, buf: bytes) -> None:
        self.ws.send(buf)

    def flush(self) -> None:
        pass
