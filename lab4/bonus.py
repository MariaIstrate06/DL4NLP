import copy
contextFreeGrammar = [
    {'LHS': 'S', 'RHS': ['NP', 'VP'], 'p': 0.8},
    {'LHS': 'S', 'RHS': ['Aux', 'NP', 'VP'], 'p': 0.1}, ## + 1 rule
    {'LHS': 'S', 'RHS': ['VP'], 'p': 0.1}, ## + _ rules
    {'LHS': 'NP', 'RHS': ['Pronoun'], 'p': 0.2}, ## + 4 rules
    {'LHS': 'NP', 'RHS': ['Proper-Noun'], 'p': 0.2}, ## + 2 rules
    {'LHS': 'NP', 'RHS': ['Det', 'Nominal'], 'p': 0.6},
    {'LHS': 'Nominal', 'RHS': ['Noun'], 'p': 0.3}, ## + 4 rules
    {'LHS': 'Nominal', 'RHS': ['Nominal', 'Noun'], 'p': 0.2},
    {'LHS': 'Nominal', 'RHS': ['Nominal', 'PP'], 'p': 0.5},
    {'LHS': 'VP', 'RHS': ['Verb'], 'p': 0.2}, ## + 3 rules
    {'LHS': 'VP', 'RHS': ['Verb', 'NP'], 'p': 0.5},
    {'LHS': 'VP', 'RHS': ['VP', 'PP'], 'p': 0.3},
    {'LHS': 'PP', 'RHS': ['Prep', 'NP'], 'p': 1.0},
    {'LHS': 'Det', 'RHS': ['the'], 'p': 0.6},
    {'LHS': 'Det', 'RHS': ['a'], 'p': 0.2},
    {'LHS': 'Det', 'RHS': ['that'], 'p': 0.1},
    {'LHS': 'Det', 'RHS': ['this'], 'p': 0.1},
    {'LHS': 'Noun', 'RHS': ['book'], 'p': 0.1},
    {'LHS': 'Noun', 'RHS': ['flight'], 'p': 0.5},
    {'LHS': 'Noun', 'RHS': ['meal'], 'p': 0.2},
    {'LHS': 'Noun', 'RHS': ['money'], 'p': 0.2},
    {'LHS': 'Verb', 'RHS': ['pay'], 'p': 0.5}, ## **
    {'LHS': 'Verb', 'RHS': ['include'], 'p': 0.2},
    {'LHS': 'Verb', 'RHS': ['prefer'], 'p': 0.3},
    {'LHS': 'Pronoun', 'RHS': ['I'], 'p': 0.5},
    {'LHS': 'Pronoun', 'RHS': ['he'], 'p': 0.1},
    {'LHS': 'Pronoun', 'RHS': ['she'], 'p': 0.1},
    {'LHS': 'Pronoun', 'RHS': ['me'], 'p': 0.3},
    {'LHS': 'Proper-Noun', 'RHS': ['Houston'], 'p': 0.8},
    {'LHS': 'Proper-Noun', 'RHS': ['NWA'], 'p': 0.2},
    {'LHS': 'Aux', 'RHS': ['does'], 'p': 1.0},
    {'LHS': 'Prep', 'RHS': ['from'], 'p': 0.25},
    {'LHS': 'Prep', 'RHS': ['to'], 'p': 0.25},
    {'LHS': 'Prep', 'RHS': ['on'], 'p': 0.1},
    {'LHS': 'Prep', 'RHS': ['near'], 'p': 0.2},
    {'LHS': 'Prep', 'RHS': ['through'], 'p': 0.2},
]

nonterminal_id = 0

def get_new_nonterminal():
    global nonterminal_id
    nonterminal_id += 1
    return f'X{nonterminal_id}'

def get_rules_by_lhs(grammar):
    rules_by_lhs = dict()
    for rule in grammar:
        if rule['LHS'] not in rules_by_lhs:
            rules_by_lhs[rule['LHS']] = [rule]
        else:
            rules_by_lhs[rule['LHS']].append(rule)
    return rules_by_lhs

def convert_to_cnf(grammar):
    cnf = []

    rules_by_lhs = get_rules_by_lhs(grammar)
    print(rules_by_lhs.keys())

    rules_to_expand = []
    for rule in grammar:
        lhs = rule['LHS']
        rhs = rule['RHS']
        p = rule['p']

        if len(rhs) == 1:
            if rhs[0] in rules_by_lhs:
                # Remember to expand afterwards
                rules_to_expand.append(rule)
            else:
                # NT -> terminal
                cnf.append(rule)
        elif len(rhs) == 2:
            if (rhs[0] in rules_by_lhs) and (rhs[0] in rules_by_lhs):
                cnf.append(rule)
            else:
                new_nt = get_new_nonterminal()
                rules_by_lhs[new_nt] = [] ## Mark `new_nt` as a non-terminal.
                if (rhs[0] not in rules_by_lhs):
                    cnf.append({'LHS': copy.deepcopy(lhs), 'RHS': [copy.deepcopy(new_nt), copy.deepcopy(rhs[1])], 'p': copy.deepcopy(p)})
                    cnf.append({'LHS': copy.deepcopy(new_nt), 'RHS': [copy.deepcopy(rhs[0])], 'p': copy.deepcopy(p)})
                elif (rhs[1] not in rules_by_lhs):
                    cnf.append({'LHS': copy.deepcopy(lhs), 'RHS': [copy.deepcopy(rhs[0]), copy.deepcopy(new_nt)], 'p': copy.deepcopy(p)})
                    cnf.append({'LHS': copy.deepcopy(new_nt), 'RHS': [copy.deepcopy(rhs[1])], 'p': copy.deepcopy(p)})
        elif len(rhs) > 2:
            rule = copy.deepcopy(rule)
            new_nt = get_new_nonterminal()
            rules_by_lhs[new_nt] = [] ## Mark `new_nt` as a non-terminal.
            last_el = rule['RHS'][-1]
            cnf.append({'LHS': copy.deepcopy(rule['LHS']), 'RHS': [copy.deepcopy(new_nt), copy.deepcopy(last_el)], 'p': copy.deepcopy(p)})
            rule = {'LHS': copy.deepcopy(new_nt), 'RHS': copy.deepcopy(rule['RHS'][:-1]), 'p': 1.0}
            while len(rule['RHS']) > 2:
                # If nonterminal, add a new rule O -> X1 NT
                new_nt = get_new_nonterminal()
                rules_by_lhs[new_nt] = [] ## Mark `new_nt` as a non-terminal.
                last_el = rule['RHS'][-1]
                cnf.append({'LHS': copy.deepcopy(rule['LHS']), 'RHS': [copy.deepcopy(new_nt), copy.deepcopy(last_el)], 'p': 1.0})
                rule = {'LHS': copy.deepcopy(new_nt), 'RHS': copy.deepcopy(rule['RHS'][:-1]), 'p': 1.0}
            if len(rule['RHS']) == 2:
                rhs = rule['RHS']
                if (rhs[0] in rules_by_lhs) and (rhs[0] in rules_by_lhs):
                    cnf.append(rule)
                else:
                    new_nt = get_new_nonterminal()
                    rules_by_lhs[new_nt] = [] ## Mark `new_nt` as a non-terminal.
                    if (rhs[0] not in rules_by_lhs):
                        cnf.append({'LHS': copy.deepcopy(lhs), 'RHS': [copy.deepcopy(new_nt), copy.deepcopy(rhs[1])], 'p': copy.deepcopy(p)})
                        cnf.append({'LHS': copy.deepcopy(new_nt), 'RHS': [copy.deepcopy(rhs[0])], 'p': copy.deepcopy(p)})
                    elif (rhs[1] not in rules_by_lhs):
                        cnf.append({'LHS': copy.deepcopy(lhs), 'RHS': [copy.deepcopy(rhs[0]), copy.deepcopy(new_nt)], 'p': copy.deepcopy(p)})
                        cnf.append({'LHS': copy.deepcopy(new_nt), 'RHS': [copy.deepcopy(rhs[1])], 'p': copy.deepcopy(p)})
            else:
                raise Exception("oops" + rule)
        else:
            raise Exception("oo")
    rules_by_lhs = get_rules_by_lhs(cnf)
    if len(list(filter(lambda rul: isIncorrect(rul, rules_by_lhs), cnf))) > 0:
        raise Exception(rule, cnf[-10:])

    ## Merging rules like NT -> NT
    for i, rule in enumerate(rules_to_expand):
        lhs = rule['LHS']
        rhs = rule['RHS']
        p = rule['p']

        if len(rhs) == 1 and (rhs[0] in rules_by_lhs.keys()):
            print("Merging rules of ", rule)
            target = rhs[0]
            if target in rules_by_lhs:
                for target_rule in rules_by_lhs[target]:
                    cnf.append({
                        'LHS': lhs,
                        'RHS': target_rule['RHS'],
                        'p': p * target_rule['p']
                    })
            else:
                cnf.append(rule)
        else:
            cnf.append(rule)

    # Test
    cnf.sort(key=lambda a: a['LHS'])
    rules_by_lhs = get_rules_by_lhs(cnf)
    print('=' * 80)
    for rule in cnf:
        isIncorrect(rule, rules_by_lhs=rules_by_lhs)
    print('=' * 80)
    for rule_lhs in rules_by_lhs.keys():
        s = sum(map(lambda a: a['p'], rules_by_lhs[rule_lhs]))
        if s < 1.0:
            print("Non-1 probability: ", s, rule_lhs)
    print('=' * 80)
    return cnf

def isIncorrect(rule, rules_by_lhs):
        if not (rule['LHS'] in rules_by_lhs):
            print('!' * 20, 'Incorrect(1): ', rule)
            return True
        elif len(rule['RHS']) == 1 and (rule['RHS'][0] in rules_by_lhs):
            print('!' * 20, 'Incorrect(2): ', rule, rules_by_lhs.keys())
            return True
        elif len(rule['RHS']) == 2 and ((rule['RHS'][0] not in rules_by_lhs) or 
                (rule['RHS'][1] not in rules_by_lhs)):
            print('!' * 20, 'Incorrect(3): ', rule, rules_by_lhs.keys())
            return True
        return False

cnf_grammar = convert_to_cnf(contextFreeGrammar)
for rule in cnf_grammar:
    print(f"{rule['LHS']:<15} -> {str(rule['RHS']):<25} (p={rule['p']:<5})")

print(f"Original grammar has {len(contextFreeGrammar)} rules")
print(f"CNF      grammar has {len(cnf_grammar)} rules")