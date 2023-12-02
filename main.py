import os
from source import fp_growth

if __name__ == '__main__':
    # settings
    args = {
        "data file": "mushroom.dat",
        "minimum support": 0.1,
        "minimum confidence": 0.8,
        "limit": 10,
        "write file": True,
        "parallel processing": "auto" # "always", "never", others = "auto"
    }
    
    freq, rule = fp_growth.fp_growth_from_file(args)
    
    if args["write file"]:
        print("\nfrequency item set:")
        for item in freq[1].items():
            print('|L^{}|={}'.format(item[0], item[1]))
        print("\nassociation rules: {}".format(rule[1]))
        fp_growth.write_in_file(freq, rule, args, fp_growth.get_time())
    else:
        print("\nfrequency item set:")
        for item in freq.items():
            print('|L^{}|={}'.format(item[0], item[1]))
        print("\nassociation rules: {}".format(rule))
