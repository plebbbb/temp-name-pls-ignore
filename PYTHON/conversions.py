##TESTING STUFF AT BOTTOM
import codon
import random

#turns an int into its coorsponding char
def calc_char(x) :
    return {
        0 : 'A',
        1 : 'C',
        2 : 'G',
        3 : 'T'
    }.get(x)

#turns a char back into its binary value as an int
def calc_byte(x) : 
    return {
        'A' : 0,
        'C' : 1,
        'G' : 2,
        'T' : 3
    }.get(x)

#output is in little endian, will work with any group of bytes
def bytestring_to_letterstring(dataset) : 
    output = ""
    for byte in dataset.encode() :
       # output_ints(byte)
        for i in range(0,4) : 
            twobits = (byte >> ((i*2))) & 3 #rightshift until selected bits are in the first two bits, then mask with 3 to remove other bits
           # print(twobits)
            output += calc_char(twobits)
    return output



#takes a string of 4 characters and returns an int
#reads little endian
def letter4char_to_byteint(input_4string) : 
    output = 0
    iter = 0
    for char in input_4string :
        twobits = calc_byte(char) << (iter)
        output += twobits
        iter+=2
    return output

#takes a string of characters, turns them into a string storing our data in utf8
#this string is assumed to have a length of a multiple of 4, given that one byte is 4 letters
def letterstring_to_bytestring(input_string) :
    output = ""
    for index in range(0, len(input_string)-3, 4): 
        output += chr(letter4char_to_byteint(input_string[index : index+4]))
    return output

#xors a input string with a key string. Use this to convert the raw binary string into a processed binary string
#which is ready for conversion into letter format
#it can also be used backwards to unconvert the binary string you get from converting your letter string back to its binary string form
def mask_key(input_bytestring, Mkeystring) :
    masksz = len(Mkeystring)
    bytekey = Mkeystring.encode()
    maskiter = 0
    output = ""
    for char in input_bytestring.encode() :
        output += chr(char ^ bytekey[maskiter])
        maskiter+=1
        if(masksz == maskiter):
            maskiter = 0
    return output


def iter_check(str):
    for i in range(1,len(str)-4):
        if str[i : i+3] in codon.codonlist:
            return False
    return True


#randomize string to not have any codons via brute force
#mistakes were made
def codon_hard_randomize(SVV):
    output = ""
    for e in range(0,random.randint(2,10)):
        output += calc_char(random.randint(0,3))           
    check_str = SVV + output + SVV
    while(not iter_check(check_str)):
        output = ""
        for e in range(0,random.randint(2,10)):
            output += calc_char(random.randint(0,3))       
        check_str = SVV + output + SVV
    return output


#corrects for randomly generated codons by doing a blank gap with random letters
def codon_fix_check(final_prealgo_str):
    i = 0
    lastsplit = 0
    output = ""
    while(i <= len(final_prealgo_str)-3) :
        if final_prealgo_str[i : i+3] in codon.codonlist:
            SV = final_prealgo_str[i : i+3]
            output += final_prealgo_str[lastsplit : i+3]
            lastsplit = i+3
            i+=3
            output += codon_hard_randomize(SV)
            output += SV
            continue
        i+=1
    if(i < len(final_prealgo_str)):
        output += final_prealgo_str[lastsplit : len(final_prealgo_str)]
    return output


#TESTS
"""
#one number test - passed
data = (27).to_bytes(1,'big') ##00 01 10 11, or A, C, T, G
result = bytestring_to_letterstring(data)
print(f'Initial: {27}\nConverted: {result}\nUnconverted: {letter4char_to_byteint(result)}')

"""
"""
#string test - passed
init = "test123what123"
convertedinit = bytestring_to_letterstring(init.encode())
print(f'Initial: {init}\nConverted: {convertedinit}')
unconvertedval = letterstring_to_bytestring(convertedinit)
print(f'Unconverted value: {unconvertedval}')
"""
"""
#xor masking test - passed
#the first 4 characters should be all whatever utf-8's 0 is, as test would match with test
base = "testing lorem ipsum"
key = "test"
masked = mask_key(base, key)
unmasked = mask_key(masked,key)
print(f'OG: {base}\nMASKED: {masked}\nUNMASKED: {unmasked}')
"""
'''
#codon conversion test - seems ok
st = "0000TGC0000TGC0"
print(codon_fix_check(st))

'''