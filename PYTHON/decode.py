import sys
import conversions
##sys.argv[] is how you get your parameters
##just print stuff, do sys.stdout.flush() at end

#print("HI")
#print(sys.argv[1])


finaldata = conversions.mask_key(conversions.letterstring_to_bytestring(str(sys.argv[1])), str(sys.argv[2]))
print(finaldata)
sys.stdout.flush()