import sys
import conversions
##sys.argv[] is how you get your parameters
##just print stuff, do sys.stdout.flush() at end


processedsecretdata = conversions.bytestring_to_letterstring(conversions.mask_key(str(sys.argv[1]), str(sys.argv[2])))
sys.stdout.write(processedsecretdata)

sys.stdout.flush()
