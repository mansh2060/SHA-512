from initializing_hash_values import calculate_hash_values
from rounds_80_preprocessing import Splitting
from round_constants import round_function,prime_num_list

class CompressionLoop:
    def __init__(self,text,binary_encoded_list):
        _,self.hash_dict = calculate_hash_values([2,3,5,7,11,13,17,19])
        self.check_length = len(binary_encoded_list)
        splitting = Splitting(text,binary_encoded_list)
        self.first_64_bit_list,self.final_64_bit_list = splitting.break_padding_sequence()
        self.K = round_function(prime_num_list)
        self.compressed_list = []
    def sigma(self):
        summation_e = (int(str(self.hash_dict["e"]), 16) >> 14) ^ (int(str(self.hash_dict["e"]),16)>> 18) ^ (int(str(self.hash_dict["e"]),16)>> 41)
        summation_a = (int(str(self.hash_dict["a"]), 16) >> 28) ^ (int(str(self.hash_dict["a"]), 16) >> 34) ^ (int(str(self.hash_dict["a"]), 16) >> 39)
        return summation_e, summation_a
    
    def choose(self):
        Ch = (int(str(self.hash_dict["e"]),16) & int(str(self.hash_dict["f"]),16)) ^ (~int(str(self.hash_dict["e"]),16) & int(str(self.hash_dict["g"]),16))
        return Ch
    
    def majority(self):
        Maj = (int(str(self.hash_dict["a"]),16) & int(str(self.hash_dict["b"]),16)) ^ (int(str(self.hash_dict["a"]),16) & int(str(self.hash_dict["c"]),16)) ^ (int(str(self.hash_dict["b"]),16) & int(str(self.hash_dict["c"]),16))
        return Maj
    
    def variables(self,i,hexa_decimal_value):
        summation_e,summation_a = self.sigma()
        Ch = self.choose()
        Maj = self.majority()
        T1 = int(str(self.hash_dict["h"]), 16) + summation_e + Ch + int(str(self.K[i]), 16) + hexa_decimal_value
        T2 = summation_a + Maj
        self.hash_dict["h"] = self.hash_dict["g"]
        self.hash_dict["g"] = self.hash_dict["f"]
        self.hash_dict["f"] = self.hash_dict["e"]
        self.hash_dict["e"] = (int(str(self.hash_dict["d"]),16) + T1) % (2**64)
        self.hash_dict["d"] = self.hash_dict["c"]
        self.hash_dict["c"] = self.hash_dict["b"] 
        self.hash_dict["b"] = self.hash_dict["a"]
        self.hash_dict["a"] = (T1 + T2) % (2 ** 64)
        return self.hash_dict["a"],self.hash_dict["b"],self.hash_dict["c"],self.hash_dict["d"],self.hash_dict["e"],self.hash_dict["f"],self.hash_dict["g"],self.hash_dict["h"]
               
    
    def compression(self):
        a, b, c, d, e, f, g, h = 0, 0, 0, 0, 0, 0, 0, 0
        if self.check_length < 896:
            for i in range(len(self.first_64_bit_list)):
               binary_string = ''.join(str(element) for element in self.first_64_bit_list[i])
               integer_value = int(binary_string,2)
               hexa_decimal_value = hex(integer_value)
               a,b,c,d,e,f,g,h = self.variables(i,int(hexa_decimal_value,16))
            self.compressed_list.append(a)
            self.compressed_list.append(b)
            self.compressed_list.append(c)
            self.compressed_list.append(d)
            self.compressed_list.append(e)
            self.compressed_list.append(f)
            self.compressed_list.append(g)
            self.compressed_list.append(h)
            return self.compressed_list
    
        elif 896 < self.check_length < 1024 :
            for i in range(len(self.first_64_bit_list)):
               binary_string = ''.join(str(element) for element in self.first_64_bit_list[i])
               integer_value = int(binary_string,2)
               hexa_decimal_value = hex(integer_value)
               a,b,c,d,e,f,g,h = self.variables(i,int(hexa_decimal_value,16))
            self.compressed_list.append(a)
            self.compressed_list.append(b)
            self.compressed_list.append(c)
            self.compressed_list.append(d)
            self.compressed_list.append(e)
            self.compressed_list.append(f)
            self.compressed_list.append(g)
            self.compressed_list.append(h)
            for j in range(len(self.final_64_bit_list)):
                binary_string = ''.join(str(element) for element in self.first_64_bit_list[j])
                integer_value = int(binary_string,2)
                hexa_decimal_value = hex(integer_value)
                a1,b1,c1,d1,e1,f1,g1,h1 = self.variables(j,int(hexa_decimal_value,16))
            self.compressed_list.append(a1)
            self.compressed_list.append(b1)
            self.compressed_list.append(c1)
            self.compressed_list.append(d1)
            self.compressed_list.append(e1)
            self.compressed_list.append(f1)
            self.compressed_list.append(g1)
            self.compressed_list.append(h1)
            return self.compressed_list
                
        elif self.check_length % 1024 == 0:
            num_blocks = self.check_length // 1024
            i = 0
            while i < num_blocks:
                for j in range(len(self.first_64_bit_list[i])):
                    binary_string = ''.join(str(element) for element in self.first_64_bit_list[i][j])
                    integer_value = int(binary_string,2)
                    hexa_decimal_value = hex(integer_value)
                    a,b,c,d,e,f,g,h = self.variables(i,int(hexa_decimal_value,16))
                self.compressed_list.append(a)
                self.compressed_list.append(b)
                self.compressed_list.append(c)
                self.compressed_list.append(d)
                self.compressed_list.append(e)
                self.compressed_list.append(f)
                self.compressed_list.append(g)
                self.compressed_list.append(h)
                i += 1
            for k in range(len(self.final_64_bit_list)):
                binary_string = ''.join(str(element) for element in self.final_64_bit_list[k])
                integer_value = int(binary_string,2)
                hexa_decimal_value = hex(integer_value)
                a,b,c,d,e,f,g,h = self.variables(j,int(hexa_decimal_value,16))
            self.compressed_list.append(a)
            self.compressed_list.append(b)
            self.compressed_list.append(c)
            self.compressed_list.append(d)
            self.compressed_list.append(e)
            self.compressed_list.append(f)
            self.compressed_list.append(g)
            self.compressed_list.append(h)
            return self.compressed_list

        else:
            num_blocks = self.check_length // 1024
            i = 0
            while i < num_blocks:
                for j in range(len(self.first_64_bit_list[i])):
                    binary_string = ''.join(str(element) for element in self.first_64_bit_list[i][j])
                    integer_value = int(binary_string,2)
                    hexa_decimal_value = hex(integer_value)
                    a,b,c,d,e,f,g,h = self.variables(i,int(hexa_decimal_value,16))
                self.compressed_list.append(a)
                self.compressed_list.append(b)
                self.compressed_list.append(c)
                self.compressed_list.append(d)
                self.compressed_list.append(e)
                self.compressed_list.append(f)
                self.compressed_list.append(g)
                self.compressed_list.append(h)
                i += 1
            for k in range(len(self.final_64_bit_list)):
                binary_string = ''.join(str(element) for element in self.final_64_bit_list[k])
                integer_value = int(binary_string,2)
                hexa_decimal_value = hex(integer_value)
                a,b,c,d,e,f,g,h = self.variables(j,int(hexa_decimal_value,16))
            self.compressed_list.append(a)
            self.compressed_list.append(b)
            self.compressed_list.append(c)
            self.compressed_list.append(d)
            self.compressed_list.append(e)
            self.compressed_list.append(f)
            self.compressed_list.append(g)
            self.compressed_list.append(h)
            return self.compressed_list




    
