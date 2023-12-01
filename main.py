import os
from source import fp_growth

if __name__ == '__main__':
    # settings
    args = {
        "data file": "mushroom.dat",
        "minimum support": 0.1,
        "minimum confidence": 0.8,
        "limit": 5,
        "write file": False,
        "parallel processing": "auto" # "always", "never", others = "auto"
    }
    
    freq, rule = fp_growth.fp_growth_from_file(args.values())
    
    if args["write file"]:
        print("\nfrequency item set: {}".format(freq[1]))
        print("association rules: {}".format(rule[1]))
        fp_growth.write_in_file(freq, rule, args, fp_growth.get_time())
    else:
        print("\nfrequency item set: {}".format(freq))
        print("association rules: {}".format(rule))