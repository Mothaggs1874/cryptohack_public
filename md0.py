from pwn import *
import json
from Crypto.Util.number import long_to_bytes, bytes_to_long
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def bxor(a, b):
    return bytes(x ^ y for x, y in zip(a, b))


def hash(data, u):
    data = pad(data, 16)
    out = u
    for i in range(0, len(data), 16):
        blk = data[i:i+16]
        out = bxor(AES.new(blk, AES.MODE_ECB).encrypt(out), out)
    return out


HOST = "socket.cryptohack.org"
PORT = 13388

r = remote(HOST, PORT)


def json_recv():
    line = r.readline()
    return json.loads(line.decode())

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

# use recvline or recvuntil
print(r.readline())

request = {
    "option" : "sign",
    "message" : b"1".hex(),
}

json_send(request)
response = json_recv()
signature = bytes.fromhex(response["signature"])

forged_signature = hash(b"admin=True", signature)
m = pad(b"1", 16) + b"admin=True"

request = {
    "option" : "get_flag",
    "message" : m.hex(),
    "signature" : forged_signature.hex(),
}
json_send(request)
print(json_recv())

r.close()