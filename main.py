import os
from source import fp_growth

if __name__ == '__main__':
    # settings
    file_name = "mushroom.dat"
    minimum_support = 0.1
    minimum_confindent = 0.8
    limit = 10
    return_count_only = True
    parallel_processing = "auto" # auto always never
    
    freq, rule = fp_growth.fp_growth_from_file(
        name=file_name, 
        minimum_support=minimum_support, 
        minimum_confidence=minimum_confindent, 
        limits=limit, 
        return_count_only=return_count_only, 
        parallel=parallel_processing)
    
    if return_count_only:
        print("frequency item set: {}".format(freq))
        print("association rules: {}".format(rule))
    else:
        print("frequency item set: {}".format(freq[1]))
        print("association rules: {}".format(rule[1]))
    
    for name, timer in fp_growth.get_time():
        print(name, timer)