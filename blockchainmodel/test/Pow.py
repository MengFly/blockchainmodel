from hashlib import sha256

x = 5
y = 0  # we don't know what y should be yet...
while sha256(f'{x*y}'.encode()).hexdigest()[-1] != "0":
    y += 1
hash_result = sha256(str(x * y).encode()).hexdigest()
print(f'The solution is y = {y}, The hash_result is : f{hash_result}')

