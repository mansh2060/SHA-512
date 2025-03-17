"""
Algorithm:
1024 // 16  ---> 64 bits
0 - 15 
15 - 80 expand using 0-15
the equation used to expan is 
W t = sigma(W (t-2)) + W(t-7) + sigma(W(t -15)) + W(t-16)
sigma(W(t-2)) = W(t-2) >> 19 ^ W(t-2) >> 61 ^ W(t-2) >> 6
sigma(W(t-15)) = W(t-15) >> 1 ^ W(t-15) >> 8 ^ W(t-15) >> 7
"""
from text_to_padding import Padding
import sys
sys.set_int_max_str_digits(10000)
class Splitting:
    def __init__(self,text,binary_encoded_list):
        self.text = text
        self.binary_encoded_list = binary_encoded_list
        self.length_check = len(binary_encoded_list)
        padding = Padding(text,binary_encoded_list)
        self.first_block,self.final_block=padding.binary_to_padding()
        self.first_64_bit_list = []
        self.final_64_bit_list = []
    
    def break_padding_sequence(self):  # 1024 ---> 64 bits , (16 ,0-15) + (15-79) 
        
        if self.length_check < 896:
            for i in range(0,len(self.first_block),64):
                self.first_64_bit_list.append(self.first_block[i:i+64])
            k = 16
            while k < 80:
                num_int_2 = int(''.join([str(element) for element in self.first_64_bit_list[k-2]]))
                sigma1_k_2 = (num_int_2 >> 19) ^ (num_int_2 >> 61) ^ (num_int_2 >> 6)
                num_int_15 = int(''.join([str(element) for element in self.first_64_bit_list[k-15]]))
                sigma0_k_15 = (num_int_15 >> 1) ^ (num_int_15 >> 8) ^ (num_int_15 >> 7)
                list1_int = int(''.join([str(element) for element in self.first_64_bit_list[k-7]]))
                list2_int = int(''.join([str(element) for element in self.first_64_bit_list[k-16]]))
                w_k = (sigma1_k_2 + list1_int + sigma0_k_15 + list2_int) % (2**64)
                self.first_64_bit_list.append([int(bit) for bit in bin(w_k)[2:].zfill(64)])
                k += 1
            return self.first_64_bit_list,None
        
        elif 896 < self.length_check < 1024:
            for i in range(0,len(self.first_block),64):     # first block 
                self.first_64_bit_list.append(self.first_block[i:i+64])
            k = 16
            while k < 80:
                num_int_2 = int(''.join([str(element) for element in self.first_64_bit_list[k-2]]))
                sigma1_k_2 = (num_int_2 >> 19) ^ (num_int_2 >> 61) ^ (num_int_2 >> 6)
                num_int_15 = int(''.join([str(element) for element in self.first_64_bit_list[k-15]]))
                sigma0_k_15 = (num_int_15 >> 1) ^ (num_int_15 >> 8) ^ (num_int_15 >> 7)
                list1_int = int(''.join([str(element) for element in self.first_64_bit_list[k-7]]))
                list2_int = int(''.join([str(element) for element in self.first_64_bit_list[k-16]]))
                w_k = (sigma1_k_2 + list1_int + sigma0_k_15 + list2_int) % (2**64)
                self.first_64_bit_list.append([int(bit) for bit in bin(w_k)[2:].zfill(64)])
                k += 1
            
            for j in range(0,len(self.final_block),64):      # final block
                self.final_64_bit_list.append(self.final_block[j:j+64])
            h = 16
            while h < 80:
                num_int_2 = int(''.join([str(element) for element in self.final_64_bit_list[h-2]]))
                sigma1_k_2 = (num_int_2 >> 19) ^ (num_int_2 >> 61) ^ (num_int_2 >> 6)
                num_int_15 = int(''.join([str(element) for element in self.final_64_bit_list[h-15]]))
                sigma0_k_15 = (num_int_15 >> 1) ^ (num_int_15 >> 8) ^ (num_int_15 >> 7)
                list1_int = int(''.join([str(element) for element in self.final_64_bit_list[h-7]]))
                list2_int = int(''.join([str(element) for element in self.final_64_bit_list[h-16]]))
                w_k = (sigma1_k_2 + list1_int + sigma0_k_15 + list2_int) % (2**64)
                self.final_64_bit_list.append([int(bit) for bit in bin(w_k)[2:].zfill(64)])
                h += 1
            
            return self.first_64_bit_list , self.final_64_bit_list
        
        elif self.length_check % 1024 == 0:
            num_blocks = self.length_check // 1024
            first_blocks = [self.binary_encoded_list[i*1024 :(i+1) * 1024] for i in range(num_blocks)]
            for block in first_blocks:
                block_list = [block[j:j+64] for j in range(0,1024,64)]
                self.first_64_bit_list.append(block_list)
            k = 0
            while k < num_blocks:
                h = 16
                while h < 80 :
                    num_int_2 = int(''.join([str(element) for element in self.first_64_bit_list[k][h-2]]))
                    sigma1_k_2 = (num_int_2 >> 19) ^ (num_int_2 >> 61) ^ (num_int_2 >> 6)
                    num_int_15 = int(''.join([str(element) for element in self.first_64_bit_list[k][h-15]]))
                    sigma0_k_15 = (num_int_15 >> 1) ^ (num_int_15 >> 8) ^ (num_int_15 >> 7)
                    list1_int = int(''.join([str(element) for element in self.first_64_bit_list[k][h-7]]))
                    list2_int = int(''.join([str(element) for element in self.first_64_bit_list[k][h-16]]))
                    w_k = (sigma1_k_2 + list1_int + sigma0_k_15 + list2_int) % (2**64)
                    self.first_64_bit_list[k].append([int(bit) for bit in bin(w_k)[2:].zfill(64)])
                    h += 1
                k += 1
            for j in range(0,len(self.final_block),64):
                self.final_64_bit_list.append(self.final_block[j:j+64])
            m = 16
            while m < 80:
                num_int_2 = int(''.join([str(element) for element in self.final_64_bit_list[m-2]]))
                sigma1_k_2 = (num_int_2 >> 19) ^ (num_int_2 >> 61) ^ (num_int_2 >> 6)
                num_int_15 = int(''.join([str(element) for element in self.final_64_bit_list[m-15]]))
                sigma0_k_15 = (num_int_15 >> 1) ^ (num_int_15 >> 8) ^ (num_int_15 >> 7)
                list1_int = int(''.join([str(element) for element in self.final_64_bit_list[m-7]]))
                list2_int = int(''.join([str(element) for element in self.final_64_bit_list[m-16]]))
                w_k = (sigma1_k_2 + list1_int + sigma0_k_15 + list2_int) % (2**64)
                self.final_64_bit_list.append([int(bit) for bit in bin(w_k)[2:].zfill(64)])
                m += 1
            return self.first_64_bit_list , self.final_64_bit_list
        
        else:
            num_blocks = self.length_check // 1024
            first_blocks = [self.binary_encoded_list[i * 1024 : (i+1) * 1024] for i in range(num_blocks)]
            for block in first_blocks:
                block_list = [block[j:j+64] for j in range(0,1024,64)]
                self.first_64_bit_list.append(block_list)
            k = 0
            while k < num_blocks:
                h = 16
                while h < 80 :
                    num_int_2 = int(''.join([str(element) for element in self.first_64_bit_list[k][h-2]]))
                    sigma1_k_2 = (num_int_2 >> 19) ^ (num_int_2 >> 61) ^ (num_int_2 >> 6)
                    num_int_15 = int(''.join([str(element) for element in self.first_64_bit_list[k][h-15]]))
                    sigma0_k_15 = (num_int_15 >> 1) ^ (num_int_15 >> 8) ^ (num_int_15 >> 7)
                    list1_int = int(''.join([str(element) for element in self.first_64_bit_list[k][h-7]]))
                    list2_int = int(''.join([str(element) for element in self.first_64_bit_list[k][h-16]]))
                    w_k = (sigma1_k_2 + list1_int + sigma0_k_15 + list2_int) % (2**64)
                    self.first_64_bit_list[k].append([int(bit) for bit in bin(w_k)[2:].zfill(64)])
                    h += 1
                k += 1
            for j in range(0,len(self.final_block),64):
                self.final_64_bit_list.append(self.final_block[j:j+64])
            m = 16
            while m < 80:
                num_int_2 = int(''.join([str(element) for element in self.final_64_bit_list[m-2]]))
                sigma1_k_2 = (num_int_2 >> 19) ^ (num_int_2 >> 61) ^ (num_int_2 >> 6)
                num_int_15 = int(''.join([str(element) for element in self.final_64_bit_list[m-15]]))
                sigma0_k_15 = (num_int_15 >> 1) ^ (num_int_15 >> 8) ^ (num_int_15 >> 7)
                list1_int = int(''.join([str(element) for element in self.final_64_bit_list[m-7]]))
                list2_int = int(''.join([str(element) for element in self.final_64_bit_list[m-16]]))
                w_k = (sigma1_k_2 + list1_int + sigma0_k_15 + list2_int) % (2**64)
                self.final_64_bit_list.append([int(bit) for bit in bin(w_k)[2:].zfill(64)])
                m += 1
            return self.first_64_bit_list , self.final_64_bit_list
        
