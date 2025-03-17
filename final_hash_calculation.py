"""
Flow of code
converting_text_to_binary  (converting_to_binary)
padding the binary encoded text and converting them equal block of 1024 (text_to_padding)
breaking 1024 bits padded sequence to 64 bits (16 parts)(0--15) ---> (15-79) from (0-15) (rounds_80_preprocessing)
from 8 primes calculated the 8 hash values(initializing_hash_values)
calculating the round constants(round_constants)
calculating compression function
calculating the final hash values  
"""

from compression_function import CompressionLoop
from initializing_hash_values import calculate_hash_values


class HashCalculation:
    def __init__(self,text,binary_encoded_list):
        self.text = text
        self.binary_encoded_list = binary_encoded_list
        self.check_sum = len(binary_encoded_list)
        compressionloop = CompressionLoop(text,binary_encoded_list)
        self.compressed_list = compressionloop.compression()
        self.hash_list,_ = calculate_hash_values([2,3,5,7,11,13,17,19])
        self.hash_hex_list = []
        
    def hash_calulation(self):
        if self.check_sum < 896:
            for i in range(len(self.compressed_list)):
                hash_int = int(str(self.hash_list[i]),16) + self.compressed_list[i]
                hash_hex = hex(hash_int)
                self.hash_hex_list.append(hash_hex)
            return self.hash_hex_list
        
        elif 896 < self.check_sum < 1024:
            for i in range(0,len(self.compressed_list),8):
                x = self.compressed_list[i:i+8]
                for j in range(len(x)):
                    hash_int = int(str(self.hash_list[j]),16) + x[j]
                    hash_hex = hex(hash_int)
                    self.hash_hex_list.append(hash_hex)
            return self.hash_hex_list
        
        elif self.check_sum % 1024 == 0:
            for i in range(0,len(self.compressed_list),8):
                x = self.compressed_list[i:i+8]
                for j in range(len(x)):
                    hash_int = int(str(self.hash_list[j]),16) + x[j]
                    hash_hex = hex(hash_int)
                    self.hash_hex_list.append(hash_hex)
            return self.hash_hex_list

        else:
            for i in range(0,len(self.compressed_list),8):
                x = self.compressed_list[i:i+8]
                for j in range(len(x)):
                    hash_int = int(str(self.hash_list[j]),16) + x[j]
                    hash_hex = hex(hash_int)
                    self.hash_hex_list.append(hash_hex)
            return self.hash_hex_list

from converting_to_binary import convert_text_to_binary 
text = """Hello I am Manish Checks message length to determine how many 1024-bit chunks need processing.
        Iterates through each chunk to perform SHA-512 round computations 80 rounds.
        Updates compressed_list with the final hash values."""
binary_encoded_list = convert_text_to_binary(text)
print(len(binary_encoded_list))
hash_calculation = HashCalculation(text,binary_encoded_list)
print(hash_calculation.hash_calulation())