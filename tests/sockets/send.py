import socket
from urllib.parse import urlparse

import numpy as np

remote = "upd://localhost:31415"
url = urlparse(remote)

print(url.hostname)
print(url.port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((url.hostname, url.port))

# sent some text
sock.send(bytes("hello", "ascii"))

arr = np.arange(0, 10)
print(arr)

sock.send(arr.tobytes())
