import os
from source import fp_growth

if __name__ == '__main__':
    # settings
    args = {
        "data file": "mushroom.dat",
        "minimum support": 0.1,
        "minimum confident": 0.8,
        "limit": 10,
        "write file": True,
        "parallel processing": "auto"
    }
    
    freq, rule = fp_growth.fp_growth_from_file(args.values())
    
    if args["write file"]:
        print("frequency item set: {}".format(freq[1]))
        print("association rules: {}".format(rule[1]))
    else:
        print("frequency item set: {}".format(freq))
        print("association rules: {}".format(rule))
    
    print()
    
    for name, timer in fp_growth.get_time():
        print(name, timer)
        
    if args["write file"]:
        fp_growth.write_in_file(freq, rule, args, fp_growth.get_time())