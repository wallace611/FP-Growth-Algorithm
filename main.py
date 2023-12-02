from source import fp_growth
import threading

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
    
    freq, rule = fp_growth.fp_growth_from_file(args)
    
    if args["write file"]:
        thread_write_file = threading.Thread(target=fp_growth.write_in_file, args=(freq, rule, args, fp_growth.get_time()))
        thread_write_file.start()
        freq = freq[1]
        rule = rule[1]
    
    print('\nResults:')
    print("\n\tfrequency item set:\n")
    for item in freq.items():
        print('\t' + '\t|L^{}|={}'.format(item[0], item[1]).expandtabs(4))
    print("\n\tassociation rules: {}".format(rule))

    try:
        thread_write_file.join()
        print('done :D')
    except:
        print('done!')