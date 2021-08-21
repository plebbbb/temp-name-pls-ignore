import sys
import conversions
##sys.argv[] is how you get your parameters
##just print stuff, do sys.stdout.flush() at end


#print("HI")
#print(sys.argv[1])
print(conversions.bytestring_to_letterstring(str(sys.argv[1])))
sys.stdout.flush()
