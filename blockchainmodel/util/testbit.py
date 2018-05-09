from blockchainmodel.util import hash
from time import time

ver = "01000000"
prehash = "81cd02ab7e569e8bcd9317e2fe99f2de44d49ab2b8851ba4a308000000000000"
mrkl_root = "e320b6c2fffc8d750423db8b1eb942ae710e951ed797f7affc8892b0f1fc122b"
timeres = "1231731025"
bits = "f2b9441a"
nonce = "42a14695"
print(time())
a = ""
print(hash.hash_proof(16))

# print(hash.hash2("MengFly"))
print(hash.byte2hex(timeres))

