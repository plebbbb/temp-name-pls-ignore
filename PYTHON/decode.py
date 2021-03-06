import sys
import conversions
import codon
##sys.argv[] is how you get your parameters
##just print stuff, do sys.stdout.flush() at end


def decode_genomeline(linestring, data_index, cur_CD, data_size):
    output = ""
    compl = False
    postcdsw_ctr = 0 #counter to prevent things like TGTGT from counting as two codons
    i = 0
    #print(linestring)
    while(i <= len(linestring)-3) :
        if linestring[i : i+3] in codon.codonlist and postcdsw_ctr == 0:
            if (cur_CD == 0) :
                cur_CD = codon.codonlist[linestring[i : i+3]]
                postcdsw_ctr = 2
                output += linestring[i : i+3]
            elif (codon.codonlist[linestring[i : i+3]] == cur_CD):
                cur_CD = 0
                i+=3
                continue
        elif(postcdsw_ctr > 0): postcdsw_ctr-=1
        if cur_CD == 0 and not compl:
            output += linestring[i]
            data_index +=1
            if(data_index == data_size):
                compl = True
        i+=1
    if cur_CD == 0 and not compl:
        while(i < len(linestring)):
            output += linestring[i]
            data_index +=1
            if(data_index == data_size):
                compl = True
                break
            i+=1

    return [data_index, compl, cur_CD, output]

def decode_genomeblock(blockstring, data_index, data_size, curCD):
    output = ""
    linelist = blockstring.split('\\n')
    compl = False
    for lv in range(0, len(linelist)):
        processedline = decode_genomeline(linelist[lv].strip('\\r'), data_index, curCD, data_size)
        output += processedline[3]
        curCD = processedline[2]
        data_index = processedline[0]
        if(processedline[1]):
            compl = True
            break
    return [data_index, compl, output, curCD]


def decode_genome_header(raw_genome_fasta, key, offset, size) :
    output = ""
    data_index = 0
    blocklist = raw_genome_fasta.split('>')
    data_size = size + offset  #4 bytes to store number, 4 letters per byte
    curCD = 0
    for bv in range(0,len(blocklist)):
        if len(blocklist[bv]) <= 3: continue #skip empty
        nameblockpair = blocklist[bv].split('\\n', 1)
       # print(nameblockpair[1])
       # print("FILL\n\n\n\n")
        statusarr = decode_genomeblock(nameblockpair[1].strip('\\r'), data_index, data_size, curCD)
        data_index = statusarr[0]
        output += statusarr[2]
        curCD = statusarr[3]
        if(statusarr[1]): break
 #   print(output)
  #  print(output[offset : len(output)])
    return conversions.mask_key(conversions.letterstring_to_bytestring(output[offset : len(output)]), key)


def decode_genome(raw_genome_fasta, key) :
    output = ""
    data_index = 0
    blocklist = raw_genome_fasta.split('>')
    data_size = int.from_bytes(decode_genome_header(raw_genome_fasta, key, 0, 16).encode(), 'big') + 32 #32 for the two 4 byte * 4 letter/byte file size headers
  #  print(data_size)
    name_size = int.from_bytes(decode_genome_header(raw_genome_fasta, key, 16, 16).encode(), 'big')
   # print(name_size)
    name = decode_genome_header(raw_genome_fasta, key, 32, name_size)
    sys.stdout.write(name.strip("\r\n"))
    sys.stdout.flush()
   # print(name)
    data_offset = 32 + name_size
    data_size += name_size
    curCD = 0
    for bv in range(0,len(blocklist)):
        if len(blocklist[bv]) <= 3: continue #skip empty
        nameblockpair = blocklist[bv].split("\\n", 1)  #some weird line spacing issue is going on here

        statusarr = decode_genomeblock(nameblockpair[1].strip('\\r'), data_index, data_size, curCD)
        data_index = statusarr[0]
        output += statusarr[2]
        curCD = statusarr[3]
        if(statusarr[1]): break
   # print(output)
    return conversions.mask_key(conversions.letterstring_to_bytestring(output[data_offset : data_size]),key)

#'''
finaldata = decode_genome(str(sys.argv[1]), str(sys.argv[2]))
sys.stdout.write(finaldata)
sys.stdout.flush()
#'''

#TESTS
'''
#one line test - PASS, probably
heldline = "9876TGT543TGT21"
print(decode_genomeline(heldline, 0, 0, 7))
'''
'''
#one block test - appears to pass
block = "98TGT76\r\r\nTGT433TGT\r\r\n5400000"
print(decode_genomeblock(block, 0, 0))
'''
'''
#header decode test - PASS
fullfile = ">HSBGPG Human gene fsor bone gla protein (BGP)\r\r\r\nACTCCCGCTATCAGCCAAAAAAAAAAAAAAAAGGCCTCCCTGCCCCTCCTCATCGCTGGGCACAGCCCAGAGGGT\r\r\nATAAACAGTGCGGACTAAACTAAGACAAAAACAGCTGAGTCCTGAGCAGCAGCCCAGCGCAGCCACCGAGACACC\r\r\nATGAGAGCCCTCACACTCCTCGCCCTATTGGCCCTGGCCGCACTTTGCATCGCTGGCCAGGCAGGTGAGTGCCCC\r\r\r\nCACCTCCCCTCAGGCCGCATTGCAGTGGGGGCTGAGAGGAGGAAGCACCATGGCCCACCTCTTCTCACCCCTTTG\r\r\r\nGCTGGCAGTCCCTTTGCAGTCTAACCACCTTGTTGCAGGCTCAATCCATTTGCCCCAGCTCTGCCCTTGCAGAGG\r\r\r\nGAGAGGAGGGAAGAGCAAGCTGCCCGAGACGCAGGGGAAGGAGGATGAGGGCCCTGGGGATGAGCTGGGGTGAAC\r\r\r\nCAGGCTCCCTTTCCTTTGCAGGTGCGAAGCCCAGCGGTGCAGAGTCCAGCAAAGGTGCAGGTATGAGGATGGACC\r\r\r\nTGATGGGTTCCTGGACCCTCCCCTCTCACCCTGGTCCCTCAGTCTCATTCCCCCACTCCTGCCACCTCCTGTCTG\r\r\r\nGCCATCAGGAAGGCCAGCCTGCTCCCCACCTGATCCTCCCAAACCCAGAGCCACCTGATGCCTGCCCCTCTGCTC\r\r\r\nCACAGCCTTTGTGTCCAAGCAGGAGGGCAGCGAGGTAGTGAAGAGACCCAGGCGCTACCTGTATCAATGGCTGGG\r\r\r\nGTGAGAGAAAAGGCAGAGCTGGGCCAAGGCCCTGCCTCTCCGGGATGGTCTGTGGGGGAGCTGCAGCAGGGAGTG\r\r\r\nGCCTCTCTGGGTTGTGGTGGGGGTACAGGCAGCCTGCCCTGGTGGGCACCCTGGAGCCCCATGTGTAGGGAGAGG\r\r\r\nAGGGATGGGCATTTTGCACGGGGGCTGATGCCACCACGTCGGGTGTCTCAGAGCCCCAGTCCCCTACCCGGATCC\r\r\r\nCCTGGAGCCCAGGAGGGAGGTGTGTGAGCTCAATCCGGACTGTGACGAGTTGGCTGACCACATCGGCTTTCAGGA\r\r\r\nGGCCTATCGGCGCTTCTACGGCCCGGTCTAGGGTGTCGCTCTGCTGGCCTGGCCGGCAACCCCAGTTCTGCTCCT\r\r\r\nCTCCAGGCACCCTTCTTTCCTCTTCCCCTTGCCCTTGCCCTGACCTCCCAGCCCTATGGATGTGGGGTCCCCATC\r\r\r\nATCCCAGCTGCTCCCAAATAAACTCCAGAAG\r\r\r\n\r\r\n\r\r\n>HSGLTH1 Human theta 1-globin gene\r\r\nCCACTGCACTCACCGCACCCGGCCAATTTTTGTGTTTTTAGTAGAGACTAAATACCATATAGTGAACACCTAAGA\r\r\nCGGGGGGCCTTGGATCCAGGGCGATTCAGAGGGCCCCGGTCGGAGCTGTCGGAGATTGAGCGCGCGCGGTCCCGG\r\r\nGATCTCCGACGAGGCCCTGGACCCCCGGGCGGCGAAGCTGCGGCGCGGCGCCCCCTGGAGGCCGCGGGACCCCTG\r\r\nGCCGGTCCGCGCAGGCGCAGCGGGGTCGCAGGGCGCGGCGGGTTCCAGCGCGGGGATGGCGCTGTCCGCGGAGGA\r\r\nCCGGGCGCTGGTGCGCGCCCTGTGGAAGAAGCTGGGCAGCAACGTCGGCGTCTACACGACAGAGGCCCTGGAAAG\r\r\nGTGCGGCAGGCTGGGCGCCCCCGCCCCCAGGGGCCCTCCCTCCCCAAGCCCCCCGGACGCGCCTCACCCACGTTC\r\r\nCTCTCGCAGGACCTTCCTGGCTTTCCCCGCCACGAAGACCTACTTCTCCCACCTGGACCTGAGCCCCGGCTCCTC\r\r\nACAAGTCAGAGCCCACGGCCAGAAGGTGGCGGACGCGCTGAGCCTCGCCGTGGAGCGCCTGGACGACCTACCCCA\r\r\nCGCGCTGTCCGCGCTGAGCCACCTGCACGCGTGCCAGCTGCGAGTGGACCCGGCCAGCTTCCAGGTGAGCGGCTG\r\r\nCCGTGCTGGGCCCCTGTCCCCGGGAGGGCCCCGGCGGGGTGGGTGCGGGGGGCGTGCGGGGCGGGTGCAGGCGAG\r\r\nTGAGCCTTGAGCGCTCGCCGCAGCTCCTGGGCCACTGCCTGCTGGTAACCCTCGCCCGGCACTACCCCGGAGACT\r\r\nTCAGCCCCGCGCTGCAGGCGTCGCTGGACAAGTTCCTGAGCCACGTTATCTCGGCGCTGGTTTCCGAGTACCGCT\r\r\nGAACTGTGGGTGGGTGGCCGCGGGATCCCCAGGCGACCTTCCCCGTGTTTGAGTAAAGCCTCTCCCAGGAGCAGC\r\r\nCTTCTTGCCGTGCTCTCTCGAGGTCAGGACGCGAGAGGAAGGCGC"
letters = int.from_bytes(decode_genome_header(fullfile, "testkey", 0, 16).encode(), 'big')
print(letters)
'''
'''
#full file decode test - PASS
fullfile = ">HSBGPG Human gene for bone gla protein (BGP)\r\r\nACTCCCGCTATCAGCCACTCCCGCTATCAGCCTGCTTAACGGTGCAAACATCAAACAAGTCACACATCCCAAAAC\r\r\nTCATCAAGTTCAAAAAAAAAAAAAAAAGGCCTCCCGGACTAAACTAAGACAAAAACAGCGCAGCCACCGAGACACC\r\r\nATGAGAGCCCTCACACTCCTCGCCCTATTGGCCCTGGCCGCACTTTGCATCGCTGGCCAGGCAGGTGAGTGCCCC\r\r\r\nCACCTCCCCTCAGGCCGCATTGCAGTGGGGGCTGAGAGGAGGAAGCACCATGGCCCACCTCTTCTCACCCCTTTG\r\r\r\nGCTGGCAGTCCCTTTGCAGTCTAACCACCTTGTTGCAGGCTCAATCCATTTGCCCCAGCTCTGCCCTTGCAGAGG\r\r\r\nGAGAGGAGGGAAGAGCAAGCTGCCCGAGACGCAGGGGAAGGAGGATGAGGGCCCTGGGGATGAGCTGGGGTGAAC\r\r\r\nCAGGCTCCCTTTCCTTTGCAGGTGCGAAGCCCAGCGGTGCAGAGTCCAGCAAAGGTGCAGGTATGAGGATGGACC\r\r\r\nTGATGGGTTCCTGGACCCTCCCCTCTCACCCTGGTCCCTCAGTCTCATTCCCCCACTCCTGCCACCTCCTGTCTG\r\r\r\nGCCATCAGGAAGGCCAGCCTGCTCCCCACCTGATCCTCCCAAACCCAGAGCCACCTGATGCCTGCCCCTCTGCTC\r\r\r\nCACAGCCTTTGTGTCCAAGCAGGAGGGCAGCGAGGTAGTGAAGAGACCCAGGCGCTACCTGTATCAATGGCTGGG\r\r\r\nGTGAGAGAAAAGGCAGAGCTGGGCCAAGGCCCTGCCTCTCCGGGATGGTCTGTGGGGGAGCTGCAGCAGGGAGTG\r\r\r\nGCCTCTCTGGGTTGTGGTGGGGGTACAGGCAGCCTGCCCTGGTGGGCACCCTGGAGCCCCATGTGTAGGGAGAGG\r\r\r\nAGGGATGGGCATTTTGCACGGGGGCTGATGCCACCACGTCGGGTGTCTCAGAGCCCCAGTCCCCTACCCGGATCC\r\r\r\nCCTGGAGCCCAGGAGGGAGGTGTGTGAGCTCAATCCGGACTGTGACGAGTTGGCTGACCACATCGGCTTTCAGGA\r\r\r\nGGCCTATCGGCGCTTCTACGGCCCGGTCTAGGGTGTCGCTCTGCTGGCCTGGCCGGCAACCCCAGTTCTGCTCCT\r\r\r\nCTCCAGGCACCCTTCTTTCCTCTTCCCCTTGCCCTTGCCCTGACCTCCCAGCCCTATGGATGTGGGGTCCCCATC\r\r\r\nATCCCAGCTGCTCCCAAATAAACTCCAGAAG\r\r\r\n\r\r\n\r\n>HSGLTH1 Human theta 1-globin gene\r\r\nCCACTGCACTCACCGCACCCGGCCAATTTTTGTGTTTTTAGTAGAGACTAAATACCATATAGTGAACACCTAAGA\r\r\nCGGGGGGCCTTGGATCCAGGGCGATTCAGAGGGCCCCGGTCGGAGCTGTCGGAGATTGAGCGCGCGCGGTCCCGG\r\r\nGATCTCCGACGAGGCCCTGGACCCCCGGGCGGCGAAGCTGCGGCGCGGCGCCCCCTGGAGGCCGCGGGACCCCTG\r\r\nGCCGGTCCGCGCAGGCGCAGCGGGGTCGCAGGGCGCGGCGGGTTCCAGCGCGGGGATGGCGCTGTCCGCGGAGGA\r\r\nCCGGGCGCTGGTGCGCGCCCTGTGGAAGAAGCTGGGCAGCAACGTCGGCGTCTACACGACAGAGGCCCTGGAAAG\r\r\nGTGCGGCAGGCTGGGCGCCCCCGCCCCCAGGGGCCCTCCCTCCCCAAGCCCCCCGGACGCGCCTCACCCACGTTC\r\r\nCTCTCGCAGGACCTTCCTGGCTTTCCCCGCCACGAAGACCTACTTCTCCCACCTGGACCTGAGCCCCGGCTCCTC\r\r\nACAAGTCAGAGCCCACGGCCAGAAGGTGGCGGACGCGCTGAGCCTCGCCGTGGAGCGCCTGGACGACCTACCCCA\r\r\nCGCGCTGTCCGCGCTGAGCCACCTGCACGCGTGCCAGCTGCGAGTGGACCCGGCCAGCTTCCAGGTGAGCGGCTG\r\r\nCCGTGCTGGGCCCCTGTCCCCGGGAGGGCCCCGGCGGGGTGGGTGCGGGGGGCGTGCGGGGCGGGTGCAGGCGAG\r\r\nTGAGCCTTGAGCGCTCGCCGCAGCTCCTGGGCCACTGCCTGCTGGTAACCCTCGCCCGGCACTACCCCGGAGACT\r\r\nTCAGCCCCGCGCTGCAGGCGTCGCTGGACAAGTTCCTGAGCCACGTTATCTCGGCGCTGGTTTCCGAGTACCGCT\r\r\nGAACTGTGGGTGGGTGGCCGCGGGATCCCCAGGCGACCTTCCCCGTGTTTGAGTAAAGCCTCTCCCAGGAGCAGC\r\r\nCTTCTTGCCGTGCTCTCTCGAGGTCAGGACGCGAGAGGAAGGCGC"
letters = decode_genome(fullfile, "testkey")
print(letters)
'''