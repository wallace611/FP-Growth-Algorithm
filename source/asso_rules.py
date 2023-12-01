from itertools import chain, combinations
import multiprocessing as mp

def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))

def getSupport(testSet, itemSetList):
    count = 0
    testSet = set(testSet)
    for itemSet in itemSetList:
        if testSet.issubset(itemSet):
            count += 1
    return count

def associationRuleCount(freqItemSet, minimum_confidence):
    rules = []
    supportCache = {tuple(itemSet): support for itemSet, support in freqItemSet}
    
    for itemSet, itemSetSup in freqItemSet:
        subsets = powerset(itemSet)
        
        for s in subsets:
            if len(s) > 0:
                confidence = float(itemSetSup / supportCache.get(s, 0))
                if(confidence >= minimum_confidence):
                    rules.append([set(s), set(itemSet.difference(s)), confidence])
                    
    return rules

def calculate_confidence(args):
    itemSet, itemSetSup, minConf, supportCache, return_count = args
    subsets = powerset(itemSet)
    if return_count:
        rules = 0
    else:
        rules = []
    for s in subsets:
        if len(s) > 0:
            confidence = float(itemSetSup / supportCache.get(s, 0))
            if confidence >= minConf:
                if return_count:
                    rules += 1
                else:
                    rules.append([set(s), set(set(itemSet).difference(s)), confidence])
    return rules

def caluculate_association_rule_parallel(freqItemSet, minConf, return_count=False):
    supportCache = mp.Manager().dict()
    supportCache = {tuple(itemSet): support for itemSet, support in freqItemSet}

    pool = mp.Pool(mp.cpu_count())  # 使用 CPU 核心數量的進程池

    args_list = [(itemSet, itemSetSup, minConf, supportCache, return_count) for itemSet, itemSetSup in freqItemSet]
    results = pool.map(calculate_confidence, args_list)

    pool.close()
    pool.join()

    if return_count:
        rules = sum(results)
    else:
        rules = []
        for result in results:
            rules.extend(result)
        rules = (rules, len(rules))

    return rules

def caluculate_association_rule(freqItemSet, minConf, return_count=False):
    supportCache = {tuple(itemSet): support for itemSet, support in freqItemSet}
    if return_count:
            rules = 0
    else:
        rules = []
    for itemSet, itemSetSup in freqItemSet:
        subsets = powerset(itemSet)
        for s in subsets:
            if len(s) > 0:
                confidence = float(itemSetSup / supportCache.get(s, 0))
                if confidence >= minConf:
                    if return_count:
                        rules += 1
                    else:
                        rules.append([set(s), set(set(itemSet).difference(s)), confidence])
    if not return_count:
        rules = (rules, len(rules))

    return rules