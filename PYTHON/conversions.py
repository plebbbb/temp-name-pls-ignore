##TESTING STUFF AT BOTTOM

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
def bytes_to_string(dataset) : 
    output = ""
    for byte in dataset :
       # output_ints(byte)
        for i in range(0,4) : 
            twobits = (byte >> ((i*2))) & 3 #rightshift until selected bits are in the first two bits, then mask with 3 to remove other bits
           # print(twobits)
            output += calc_char(twobits)
    return output

#takes a string of 4 characters and returns an int
#reads little endian
def letter4_to_byte(input_4string) : 
    output = 0
    iter = 0
    for char in input_4string :
        twobits = calc_byte(char) << (iter)
        output += twobits
        iter+=2
    print(output)
    return output

#takes a string of characters, turns them into a string storing our data in utf8
#this string is assumed to have a length of a multiple of 4, given that one byte is 4 letters
def string_to_byte(input_string) :
    output = ""
    for index in range(0, len(input_string)-3, 4): 
        output += chr(letter4_to_byte(input_string[index : index+4]))
    return output

#TESTS
"""
#one number test - passed
data = (27).to_bytes(1,'big') ##00 01 10 11, or A, C, T, G
result = bytes_to_string(data)
print(f'Initial: {27}\nConverted: {result}\nUnconverted: {letter4_to_byte(result)}')

"""
"""
#string test - passed
init = "test123what123"
convertedinit = bytes_to_string(init.encode("utf8"))
print(f'Initial: {init}\nConverted: {convertedinit}')
unconvertedval = string_to_byte(convertedinit)
print(f'Unconverted value: {unconvertedval}')
"""