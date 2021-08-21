import sys
import conversions
##sys.argv[] is how you get your parameters
##just print stuff, do sys.stdout.flush() at end




"""
processedsecretdata = conversions.bytestring_to_letterstring(conversions.mask_key(str(sys.argv[1]), str(sys.argv[2])))
sys.stdout.write(processedsecretdata)
sys.stdout.flush()

"""
#check if substring in list prior to skipping
codonlist = {
    "TGT" : 1,
    "TGC" : 1
}

#returns a list consisting of the current processeddata position, and the converted string
def encode_genomeblock(substring, input_data, data_index):
    skipV = 0
    start_indexrange = 0
    outputstr = ""
    for i in range(3, len(substring)):
        if substring[i] == "\r" or substring[i] == "\n": #encode_genome should prevent \r and \n from being the start of a block
            if(skipV != 0) : 
                outputstr += substring[start_indexrange, i-1]
            else:
                dataindlength = min(substring-i-1, len(input_data) - data_index)
            start_indexrange = i
            continue
        if substring[i-3, i] in codonlist:
            if skipV == 0: 
                outputstr += substring[start_indexrange, i-1]
                start_indexrange = i
                skipV = codonlist[substring[i-3,i]]
            elif skipV != 0 and codonlist[substring[i-3,i]] == skipV :
                skipV = 0
                continue #skip this character
        if skipV != 0: continue #skip everything between pairs


    outputlist = [data_index, outputstr]
    
    return outputlist


def encode_genome(raw_genome_fasta, processeddata) :
    output = ""
    islabel = False
    codonjumpam = 0
    startind = 0
    pdataiter = 0
    for i in range(0, len(raw_genome_fasta)):
        if (raw_genome_fasta[i] == ">"):
            islabel = True
            if startind != 0: 
                outputarr =  encode_genomeblock(raw_genome_fasta[startind, i-1], processeddata, pdataiter)
                output += outputarr[1]
                pdataiter = outputarr[0]
                startind = i
            continue
        if raw_genome_fasta[i] == "\n" or raw_genome_fasta[i] == "\r":
            if islabel: 
                islabel = False
                output += raw_genome_fasta[startind, i]
                startind = i+1 #this will always be safe as we assume each label has a sequence
            continue

    outputarr =  encode_genomeblock(raw_genome_fasta[startind, i-1], processeddata, pdataiter)
    output += outputarr[1]
    pdataiter = outputarr[0]  
    return output


substring = "T\rGAACTGTGGGTGGGTGGCCGCGGGATCCCCAGGCGACCTTCCCCGTG"