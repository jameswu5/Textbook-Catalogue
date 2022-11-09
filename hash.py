# U6 Coursework
# James Wu

import math

primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,
    151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311]

class Hash:
    def __init__(self, text):
        self.__original_text = text
        self.__binary_text = None
        self.__original_length = None

        self.__hashValues = []
        self.__roundConstants = []
        self.generate_constants()

        self.__messageSchedule = []
        self.__encryptedValue = None

    # converts text into its ascii binary value
    def convert_to_binary(self):
        result = ''.join(format(ord(i), '08b') for i in self.__original_text)
        self.__binary_text = result
        self.__original_length = len(result)

    # appends a '1' to the end of the binary string generated from converting a string to binary with ascii values
    def append_one(self):
        self.__binary_text += '1'

    # pads the binary string with 0s to a length of 64 less than a multiple of 512
    def pad(self):
        current_length = len(self.__binary_text)
        length_needed = 448
        while length_needed < current_length:
            length_needed += 512
        self.__binary_text = self.__binary_text.ljust(length_needed, '0')

    # appends a 64-bit binary number representing the length of the original string
    def append_sixty_four(self):
        binary = bin(self.__original_length)[2:]
        padding = binary.zfill(64)
        self.__binary_text += padding

    # Displays the values of the attributes in the class
    def show_values(self):
        print("Original text:", self.__original_text)
        print("Binary text: ", self.__binary_text)

    # executes the first part of the hashing algorithm
    def step_one(self):
        self.convert_to_binary()
        self.append_one()
        self.pad()
        self.append_sixty_four()

    # returns a hexadecimal number based on the first 32 bits of the square/cube root of a prime
    def return_hex_prime(self, prime, order):
        constant =  hex(int(math.modf((prime)**(1/order))[0]*(1<<32)))
        if len(constant) == 9:
            temp_constant = list(constant)
            temp_constant.insert(2,"0")
            constant = "".join(temp_constant)
        return constant

    # populates the constants array and called in initialisation
    def generate_constants(self):
        for i in range(8):
            self.__hashValues.append(self.return_hex_prime(primes[i], 2))
        for j in range(64):
            self.__roundConstants.append(self.return_hex_prime(primes[j], 3))

    # Creates a message schedule of 64 32-bit words: 16 from the binary string and 32 words that are zeroed
    def create_message_schedule(self):
        for i in range(16):
            self.__messageSchedule.append(self.__binary_text[i*32:i*32+32])
        for _ in range(48):
            self.__messageSchedule.append("0"*32)

    # Shifts the whole array to the right by a certain amount, with the last elements moved to the front
    def rightrotate(self, element, shift):
        temptext = list(element)*2
        length = len(element)
        return "".join(temptext[length-shift:length*2-shift])

    # Shifts the whole array to the right by a certain amount, with 0s filling the gap at the front
    def rightshift(self, element, shift):
        length = len(element)
        temptext = list(element)
        for _ in range(length):
            temptext.insert(0,'0')
        return "".join(temptext[length-shift:length*2-shift])

    # Modifying the appended 48 32-bit words with an algorithm
    def modify_message_schedule(self):
        for i in range(16,64):
            s0_1 = self.rightrotate(self.__messageSchedule[i-15], 7)
            s0_2 = self.rightrotate(self.__messageSchedule[i-15], 18)
            s0_3 = self.rightshift(self.__messageSchedule[i-15], 3)
            s0 = '{0:b}'.format(int(s0_1,2) ^ int(s0_2,2) ^ int(s0_3,2))

            s1_1 = self.rightrotate(self.__messageSchedule[i-2], 17)
            s1_2 = self.rightrotate(self.__messageSchedule[i-2], 19)
            s1_3 = self.rightshift(self.__messageSchedule[i-2], 10)
            s1 = '{0:b}'.format(int(s1_1,2) ^ int(s1_2,2) ^ int(s1_3,2))

            self.__messageSchedule[i] = bin(int(self.__messageSchedule[i-16],2) + int(s0,2) + int(self.__messageSchedule[i-7],2) + int(s1,2) + 2**32)[-32:]

    # converts a denary number to binary without the 0b
    def to_binary(self, number):
        binary = '{0:b}'.format(number)
        return binary.zfill(32)

    def compress(self):
        # converts elements in hashValues to binary from hexadecimal and stores it in a new temporary list
        neededhashvalues = []
        for element in self.__hashValues:
            neededhashvalues.append(bin(int(element, 16))[2:].zfill(32))

        a = neededhashvalues[0]
        b = neededhashvalues[1]
        c = neededhashvalues[2]
        d = neededhashvalues[3]
        e = neededhashvalues[4]
        f = neededhashvalues[5]
        g = neededhashvalues[6]
        h = neededhashvalues[7]

        for i in range(64):
            s1_1 = self.rightrotate(e, 6)
            s1_2 = self.rightrotate(e, 11)
            s1_3 = self.rightrotate(e, 25)
            s1 = '{0:b}'.format(int(s1_1,2) ^ int(s1_2,2) ^ int(s1_3,2))

            ch = '{0:b}'.format((int(e,2) & int(f,2)) ^ ((~ int(e, 2)) & int(g,2)))
            temp1 = bin(int(h,2) + int(s1,2) + int(ch,2) + int(self.__roundConstants[i],16) + int(self.__messageSchedule[i],2) + 2**32)[-32:]

            s0_1 = self.rightrotate(a, 2)
            s0_2 = self.rightrotate(a, 13)
            s0_3 = self.rightrotate(a, 22)
            s0 = '{0:b}'.format(int(s0_1,2) ^ int(s0_2,2) ^ int(s0_3,2))

            maj = '{0:b}'.format((int(a,2) & int(b,2)) ^ (int(a,2) & int(c,2)) ^ (int(c,2) & int(b,2)))
            temp2 = bin(int(s0,2) + int(maj,2) + 2**32)[-32:]

            h = g
            g = f
            f = e
            e = bin(int(d,2) + int(temp1,2) + 2**32)[-32:]
            d = c
            c = b
            b = a
            a = bin(int(temp1,2) + int(temp2,2) + 2**32)[-32:]

        # modify final values
        h0 = hex(int(neededhashvalues[0],2) + int(a,2) + 2**32)[-8:]
        h1 = hex(int(neededhashvalues[1],2) + int(b,2) + 2**32)[-8:]
        h2 = hex(int(neededhashvalues[2],2) + int(c,2) + 2**32)[-8:]
        h3 = hex(int(neededhashvalues[3],2) + int(d,2) + 2**32)[-8:]
        h4 = hex(int(neededhashvalues[4],2) + int(e,2) + 2**32)[-8:]
        h5 = hex(int(neededhashvalues[5],2) + int(f,2) + 2**32)[-8:]
        h6 = hex(int(neededhashvalues[6],2) + int(g,2) + 2**32)[-8:]
        h7 = hex(int(neededhashvalues[7],2) + int(h,2) + 2**32)[-8:]

        # the final hash is the concatenation of all the final values
        self.__encryptedValue = h0+h1+h2+h3+h4+h5+h6+h7

    # a function performing the whole hash algorithm
    def encrypt(self):
        self.step_one()
        self.create_message_schedule()
        self.modify_message_schedule()
        self.compress()

    # a getter function returning the final hash
    def get_final_hash(self):
        return self.__encryptedValue

# a function that takes a string and returns the final hash of that string
def createhash(text):
    H = Hash(text)
    H.encrypt()
    return H.get_final_hash()