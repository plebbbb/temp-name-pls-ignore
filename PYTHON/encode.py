import sys
import conversions
import codon
##sys.argv[] is how you get your parameters
##just print stuff, do sys.stdout.flush() at end


#returns a list with the current processeddata position, activated codon, and converted string(only one line of blk)
def encode_genomeline(linestring, input_data, data_index, cur_CD):
    output = ""
    compl = False
    postcdsw_ctr = 0 #counter to prevent things like TGTGT from counting as two codons
    i = 0
    while(i <= len(linestring)-3) :
        if linestring[i : i+3] in codon.codonlist and postcdsw_ctr == 0:
            if (cur_CD == 0) :
                cur_CD = codon.codonlist[linestring[i : i+3]]
                postcdsw_ctr = 2
            elif (codon.codonlist[linestring[i : i+3]] == cur_CD):
                cur_CD = 0
                output += linestring[i : i+3]
                i+=3
                continue
        elif(postcdsw_ctr > 0): postcdsw_ctr-=1
        if cur_CD != 0 or compl:
            output += linestring[i]
        else:
            output += input_data[data_index]
            data_index +=1
            if(data_index == len(input_data)):
                compl = True
        i+=1
    if cur_CD == 0 and not compl:
        while(i < len(linestring)):
            output += input_data[data_index]
            data_index +=1
            if(data_index == len(input_data)):
                compl = True
                break
            i+=1
    else:
        output += linestring[len(linestring)-2 : len(linestring)]

    return [data_index, compl, cur_CD, output]

#returns a list consisting of the current processeddata position, and the converted string
def encode_genomeblock(blockstring, input_data, data_index):
    output = ""
    linelist = blockstring.split('\n')
    curCD = 0
    compl = False
    for lv in range(0, len(linelist)):
        processedline = encode_genomeline(linelist[lv].rstrip('\r'), input_data, data_index, curCD)
        output += processedline[3] + '\r\n'
        curCD = processedline[2]
        data_index = processedline[0]
        if(processedline[1]):
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
header = conversions.bytestring_to_letterstring(conversions.mask_key((len(processedsecretdata).to_bytes(4,'big')).decode(), str(sys.argv[3])))
finalizeddata = encode_genome(str(sys.argv[1]), header + processedsecretdata)
sys.stdout.write(finalizeddata)
sys.stdout.flush()
#""




#TESTS
'''
#one line test - passed
substring = "0000TGTTGTTGT0000"
targetstr = "987654321" # process index should be 9
outputlist = encode_genomeline(substring, targetstr, 0, 0)
print(f'CUR_INDEX: {outputlist[0]}\nCOMPLETE?: {outputlist[1]}\nIN CODON PAIR?: {outputlist[2]}PROCESSED STRING: {outputlist[3]}')
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