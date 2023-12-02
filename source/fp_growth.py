from . import asso_rules
from . import freq_item_set
import time
import os

FIS_time = 0.0
aso_time = 0.0
overall_time = 0.0

def fp_growth_from_file(args):
    name, minimum_support, minimum_confidence, limits, detailed_result, parallel = args.values()
    if parallel != 'always' and parallel != 'never':
        parallel = 'auto'
        
    print('\nSettings: ')
    for item in args.items():
        print('\t' + str(item).strip('()').replace("'", '').replace(',', ':'))
    print()
    

    global FIS_time
    global aso_time
    global overall_time
    
    # start FIS_time and overall_time
    FIS_time = overall_time = time.time()
    
    data = get_from_file(file_name=name)
    minimum_freq = int(minimum_support * len(data) + 1)

    freq_item = []
    freq_gen = freq_item_set.find_frequent_itemsets(data, minimum_freq, limit=limits)
    for itemSet, support in freq_gen:
        freq_item.append((itemSet, support))
    
    # end FIS_time
    FIS_time = time.time() - FIS_time

    print('frequency item set: ', FIS_time, 'seconds')

    #start aso_time
    aso_time = time.time()
    
    # calculating association rule
    if (len(freq_item) < 400000 and parallel == 'auto') or parallel == 'never':
        rules = asso_rules.caluculate_association_rule(freq_item, minimum_confidence, detailed_result)
    else:
        rules = asso_rules.caluculate_association_rule_parallel(freq_item, minimum_confidence, detailed_result)
    
    # end all the others timers
    end_time = time.time()
    aso_time = end_time - aso_time
    overall_time = end_time - overall_time
    
    print('assciation rules: ', aso_time, 'seconds')
    print('overall time: ', overall_time, 'seconds')
    
    return (freq_item, get_each_number(freq_item)) if detailed_result else get_each_number(freq_item), rules

def get_from_file(file_name):
    data_path = os.path.join(os.path.dirname(__file__), '..\\data\\' + file_name)
    data = []
    for line in open(data_path).readlines():
        data.append([int(x) for x in line.strip().split(' ')])

    return data

def get_each_number(freq_item_list):
    freq_item_set = {}
    for item_set, sup in freq_item_list:
        if len(item_set) in freq_item_set:
            freq_item_set[len(item_set)] += 1
        else:
            freq_item_set[len(item_set)] = 1
    return freq_item_set

def get_time():
    yield "frequency item set:", FIS_time
    yield "association rule:", aso_time
    yield "overall time:", overall_time

def write_in_file(freq_item_set, association_rule, args, time_gen):
    print("\nwriting file...")
    
    now = time.strftime("%Y-%m-%d,%H-%M-%S")
    path = os.path.join('results\\' + now + '.dat')
    file_to_write = open(path, 'x')
    
    file_to_write.write(str(now) + '\n\n')
    
    for item in args.items():
        file_to_write.write(str(item).replace("'", '').replace(',', ':').strip('()') + '\n')
    
    file_to_write.write('\nfrequency item set: ' + str(freq_item_set[1]) + '\n')
    file_to_write.write('association rules: ' + str(association_rule[1]) + '\n')
    
    for name, _time in time_gen:
        file_to_write.write('\n' + str(name) + str(_time))
    
    file_to_write.write('\n\nfrequency item set: \n')
    for itemSet in freq_item_set[0]:
        file_to_write.write(str(itemSet).strip('()') + '\n')
    
    file_to_write.write('\n\nassociation rules: \n')
    for rules in association_rule[0]:
        file_to_write.write(str(rules).strip('[]') + '\n')
    
    print("done, the file located at: \"{}\"".format(path))
