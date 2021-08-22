import sys
import conversions
import codon
##sys.argv[] is how you get your parameters
##just print stuff, do sys.stdout.flush() at end


#returns a list with the current processeddata position, activated codon, and converted string(only one line of blk)
def encode_genomeline(linestring, input_data, data_index):
    output = ""
    if(len(input_data)-data_index-1 < len(linestring)):
        output = input_data[data_index : len(input_data)] + linestring[len(input_data)-data_index-1 : len(linestring)]
        data_index = len(input_data)
    else:
        output = input_data[data_index : data_index + len(linestring)]
        data_index += len(linestring)
    return [data_index, output]

#returns a list consisting of the current processeddata position, and the converted string
def encode_genomeblock(blockstring, input_data, data_index):
    output = ""
    linelist = blockstring.split('\n')
    compl = False
    for lv in range(0, len(linelist)):
        processedline = encode_genomeline(linelist[lv].rstrip('\r'), input_data, data_index)
        output += processedline[1] + '\r\n'
        data_index = processedline[0]
        if(data_index == len(input_data)):
            compl = True
            for ev in range(lv + 1, len(linelist)):
                output += linelist[ev] + '\r\n'
            break
    return [data_index, compl, output]
##
   ## return outputlist


def encode_genome(raw_genome_fasta, processeddata) :
    output = ""
    data_index = 0
    blocklist = raw_genome_fasta.split('>')
    for bv in range(0,len(blocklist)):
        if len(blocklist[bv]) <= 3: continue #skip empty
        nameblockpair = blocklist[bv].split('\n', 1)
        statusarr = encode_genomeblock(nameblockpair[1], processeddata, data_index)
        data_index = statusarr[0]
        output += '>' + nameblockpair[0] + "\n" + statusarr[2] + "\n"
        if(statusarr[1]):
            for cv in range(bv+1, len(blocklist)):
                output += '>' + blocklist[cv]
            break
    return output


#"""
#actual processing stuff
processedsecretdata = conversions.bytestring_to_letterstring(conversions.mask_key(str(sys.argv[2]), str(sys.argv[3])))
processednamedata = conversions.bytestring_to_letterstring(conversions.mask_key(str(sys.argv[4]), str(sys.argv[3])))
headerNAME = conversions.bytestring_to_letterstring(conversions.mask_key((len(processednamedata).to_bytes(4,'big')).decode(), str(sys.argv[3])))
headerDATA = conversions.bytestring_to_letterstring(conversions.mask_key((len(processedsecretdata).to_bytes(4,'big')).decode(), str(sys.argv[3])))
finalletterdata = conversions.codon_fix_check(headerDATA + headerNAME + processednamedata + processedsecretdata)
finalizeddata = encode_genome(str(sys.argv[1]), finalletterdata)
sys.stdout.write(finalizeddata)
sys.stdout.flush()
#"""

#ACTCCCGCTATCAGCCACTCCCGCTATCAGCCCCCTCCTCATCGCTGGGCACAGCCCAGAGGGTATAAACAGATCG
#ACTCCCGCTATCAGCCACTCCCGCTATCAGCCTGCAAACATCAAACAAGTCACACATCCCAAAACTCATCAAGTTCAAAAAAAAAAAAAAAAGGCCTCCCGGACTAAACTAAGACAAAAA

#TESTS
'''
#one line test - passed
substring = "00000"
targetstr = "987654321" # process index should be 9
outputlist = encode_genomeline(substring, targetstr, 0)
print(f'CUR_INDEX: {outputlist[0]}\nPROCESSED STRING: {outputlist[1]}')
'''
'''
#multi-line test - passed
block = "00TGT000\r\r\n000TGTTGT\r\r\n0000000"
fillvals = "9876"
print(encode_genomeblock(block, fillvals, 0))
'''
'''
#full file test - passes? probably. if bugs check here
fullfile = ">HSBGPG Human gene for bone gla protein (BGP)\r\r\nGGCAGATTCCCCCTAGACCCGCCCGCACCATGGTCAGGCATGCCCCTCCTCATCGCTGGGCACAGCCCAGAGGGT\r\r\nATAAACAGTGCTGGAGGCTGGCGGGGCAGGCCAGCTGAGTCCTGAGCAGCAGCCCAGCGCAGCCACCGAGACACC\r\r\nATGAGAGCCCTCACACTCCTCGCCCTATTGGCCCTGGCCGCACTTTGCATCGCTGGCCAGGCAGGTGAGTGCCCC\r\r\nCACCTCCCCTCAGGCCGCATTGCAGTGGGGGCTGAGAGGAGGAAGCACCATGGCCCACCTCTTCTCACCCCTTTG\r\r\nGCTGGCAGTCCCTTTGCAGTCTAACCACCTTGTTGCAGGCTCAATCCATTTGCCCCAGCTCTGCCCTTGCAGAGG\r\r\nGAGAGGAGGGAAGAGCAAGCTGCCCGAGACGCAGGGGAAGGAGGATGAGGGCCCTGGGGATGAGCTGGGGTGAAC\r\r\nCAGGCTCCCTTTCCTTTGCAGGTGCGAAGCCCAGCGGTGCAGAGTCCAGCAAAGGTGCAGGTATGAGGATGGACC\r\r\nTGATGGGTTCCTGGACCCTCCCCTCTCACCCTGGTCCCTCAGTCTCATTCCCCCACTCCTGCCACCTCCTGTCTG\r\r\nGCCATCAGGAAGGCCAGCCTGCTCCCCACCTGATCCTCCCAAACCCAGAGCCACCTGATGCCTGCCCCTCTGCTC\r\r\nCACAGCCTTTGTGTCCAAGCAGGAGGGCAGCGAGGTAGTGAAGAGACCCAGGCGCTACCTGTATCAATGGCTGGG\r\r\nGTGAGAGAAAAGGCAGAGCTGGGCCAAGGCCCTGCCTCTCCGGGATGGTCTGTGGGGGAGCTGCAGCAGGGAGTG\r\r\nGCCTCTCTGGGTTGTGGTGGGGGTACAGGCAGCCTGCCCTGGTGGGCACCCTGGAGCCCCATGTGTAGGGAGAGG\r\r\nAGGGATGGGCATTTTGCACGGGGGCTGATGCCACCACGTCGGGTGTCTCAGAGCCCCAGTCCCCTACCCGGATCC\r\r\nCCTGGAGCCCAGGAGGGAGGTGTGTGAGCTCAATCCGGACTGTGACGAGTTGGCTGACCACATCGGCTTTCAGGA\r\r\nGGCCTATCGGCGCTTCTACGGCCCGGTCTAGGGTGTCGCTCTGCTGGCCTGGCCGGCAACCCCAGTTCTGCTCCT\r\r\nCTCCAGGCACCCTTCTTTCCTCTTCCCCTTGCCCTTGCCCTGACCTCCCAGCCCTATGGATGTGGGGTCCCCATC\r\r\nATCCCAGCTGCTCCCAAATAAACTCCAGAAG\r\r\n>HSGLTH1 Human theta 1-globin gene\r\r\nCCACTGCACTCACCGCACCCGGCCAATTTTTGTGTTTTTAGTAGAGACTAAATACCATATAGTGAACACCTAAGA\r\r\nCGGGGGGCCTTGGATCCAGGGCGATTCAGAGGGCCCCGGTCGGAGCTGTCGGAGATTGAGCGCGCGCGGTCCCGG\r\r\nGATCTCCGACGAGGCCCTGGACCCCCGGGCGGCGAAGCTGCGGCGCGGCGCCCCCTGGAGGCCGCGGGACCCCTG\r\r\nGCCGGTCCGCGCAGGCGCAGCGGGGTCGCAGGGCGCGGCGGGTTCCAGCGCGGGGATGGCGCTGTCCGCGGAGGA\r\r\nCCGGGCGCTGGTGCGCGCCCTGTGGAAGAAGCTGGGCAGCAACGTCGGCGTCTACACGACAGAGGCCCTGGAAAG\r\r\nGTGCGGCAGGCTGGGCGCCCCCGCCCCCAGGGGCCCTCCCTCCCCAAGCCCCCCGGACGCGCCTCACCCACGTTC\r\r\nCTCTCGCAGGACCTTCCTGGCTTTCCCCGCCACGAAGACCTACTTCTCCCACCTGGACCTGAGCCCCGGCTCCTC\r\r\nACAAGTCAGAGCCCACGGCCAGAAGGTGGCGGACGCGCTGAGCCTCGCCGTGGAGCGCCTGGACGACCTACCCCA\r\r\nCGCGCTGTCCGCGCTGAGCCACCTGCACGCGTGCCAGCTGCGAGTGGACCCGGCCAGCTTCCAGGTGAGCGGCTG\r\r\nCCGTGCTGGGCCCCTGTCCCCGGGAGGGCCCCGGCGGGGTGGGTGCGGGGGGCGTGCGGGGCGGGTGCAGGCGAG\r\r\nTGAGCCTTGAGCGCTCGCCGCAGCTCCTGGGCCACTGCCTGCTGGTAACCCTCGCCCGGCACTACCCCGGAGACT\r\r\nTCAGCCCCGCGCTGCAGGCGTCGCTGGACAAGTTCCTGAGCCACGTTATCTCGGCGCTGGTTTCCGAGTACCGCT\r\r\nGAACTGTGGGTGGGTGGCCGCGGGATCCCCAGGCGACCTTCCCCGTGTTTGAGTAAAGCCTCTCCCAGGAGCAGC\r\r\nCTTCTTGCCGTGCTCTCTCGAGGTCAGGACGCGAGAGGAAGGCGC"
print(encode_genome(fullfile, "input data test"))
'''