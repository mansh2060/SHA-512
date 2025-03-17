"""
sqrt 2,3,5,7,11,13,17,19 ---> 1.414213562,......,.....
0.414213562 into binary encoding -----> 1001,.....,....(64 bits)
64 bits binary encoding ----> hexadecimal() = result
result + add = 0x
"""
conversion_table = {
    "0000"	 : 0,
    "0001"   :   1,
    "0010"	:  2,
    "0011"  :	3,
    "0100"  :	4,
    "0101"	:  5,
    "0110"	: 6,
    "0111"  :  7,
    "1000"  :	8,
    "1001" : 	9,
    "1010"  :	'a',
    "1011"	:   'b',
    "1100"  :	'c',
    "1101"	:  'd',
    "1110"	:  'e',
    "1111"	:  'f'
}
from decimal import Decimal,getcontext   # using a inbuild library for getting non roounding off the number
def calculate_hash_values(numbers_list):
    getcontext().prec = 50
    hash_list = []
    zero_x = []
    zero_x.append(str(0))
    zero_x.append('x')
    zero_x = ''.join(zero_x)
    for num in numbers_list:
        binary_list = []
        hash_value = []
        
        sqrt_num_float = Decimal(num).sqrt()        # sqrt of 2 = 1.414213562
        sqrt_num_int = int(Decimal(num).sqrt())     # sqrt of 2 = 1
        num = sqrt_num_float - sqrt_num_int    # 0.414213562
        i = 0
        while i < 64:
            num = num * 2                      #  0.828427124
            int_num = int(num)                 #  0
            binary_list.append(int_num)        #  0,1  lenght of binary_list = 64
            num = abs((int(num) - num))
            i += 1
            
        for i in range(0,len(binary_list),4):
            binary_list_4 = binary_list[i:i+4]   # 0-4,4-8,8-12......
            key = ''.join(str(element) for element in binary_list_4)
            #key = str(key)
            value = conversion_table.get(key)
            hash_value.append(str(value))
        hash_value = "".join([element for element in hash_value])
        hash_value = zero_x + hash_value
        hash_list.append(hash_value)
    key_list = ['a','b','c','d','e','f','g','h']
    hash_dict = {}
    for idx,key_value, in enumerate(key_list):
        hash_dict[key_value] = hash_list[idx]

    return hash_list,hash_dict
        