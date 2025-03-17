from decimal import Decimal,getcontext
num_primes = 0
count = 0
num = 3
x = []
x.append(2)
while num_primes < 80:
    for i in range(2,num,1):
        if num % i == 0:
            count += 1
    if count == 0:
        x.append(num)
        num_primes += 1
    num += 1
    count = 0
prime_num_list = x[:len(x)-1]

def round_function(prime_num_list):
    K = []
    getcontext().prec = 50
    for i in range(len(prime_num_list)):
        float_num = Decimal(prime_num_list[i]) ** (Decimal(1) / Decimal(3))
        int_num = int(float_num)
        fractional_part = float_num - int_num
        integer_floor = int(fractional_part * pow(2,64))
        hex_value = hex(integer_floor)
        K.append(hex_value)
    return K

