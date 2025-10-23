import copy
contextFreeGrammar = [
    {'LHS': 'S', 'RHS': ['NP', 'VP'], 'p': 0.8},
    {'LHS': 'S', 'RHS': ['Aux', 'NP', 'VP'], 'p': 0.1},
    {'LHS': 'S', 'RHS': ['VP'], 'p': 0.1},
    {'LHS': 'NP', 'RHS': ['Pronoun'], 'p': 0.2},
    {'LHS': 'NP', 'RHS': ['Proper-Noun'], 'p': 0.2},
    {'LHS': 'NP', 'RHS': ['Det', 'Nominal'], 'p': 0.6},
    {'LHS': 'Nominal', 'RHS': ['Noun'], 'p': 0.3},
    {'LHS': 'Nominal', 'RHS': ['Nominal', 'Noun'], 'p': 0.2},
    {'LHS': 'Nominal', 'RHS': ['Nominal', 'PP'], 'p': 0.5},
    {'LHS': 'VP', 'RHS': ['Verb'], 'p': 0.2},
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

def get_non_terminals(grammar):
    rules_by_lhs = dict()
    for rule in grammar:
        if rule['LHS'] not in rules_by_lhs:
            rules_by_lhs[rule['LHS']] = [rule]
        else:
            rules_by_lhs[rule['LHS']].append(rule)
    return rules_by_lhs

def convert_to_cnf(grammar):
    cnf = []

    rules_by_lhs = get_non_terminals(grammar)

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
                if (rhs[0] not in rules_by_lhs):
                    cnf.append({'LHS': copy.deepcopy(lhs), 'RHS': [copy.deepcopy(new_nt), copy.deepcopy(rhs[1])], 'p': copy.deepcopy(p)})
                    cnf.append({'LHS': copy.deepcopy(new_nt), 'RHS': [copy.deepcopy(rhs[0])], 'p': copy.deepcopy(p)})
                elif (rhs[1] not in rules_by_lhs):
                    cnf.append({'LHS': copy.deepcopy(lhs), 'RHS': [copy.deepcopy(rhs[0]), copy.deepcopy(new_nt)], 'p': copy.deepcopy(p)})
                    cnf.append({'LHS': copy.deepcopy(new_nt), 'RHS': [copy.deepcopy(rhs[1])], 'p': copy.deepcopy(p)})
        elif len(rhs) > 2:
            while len(rhs) > 2:
                last_el = rhs[-1]
                if last_el in rules_by_lhs:
                    # If nonterminal, add a new rule O -> X1 NT
                    new_nt = get_new_nonterminal()
                    cnf.append({'LHS': copy.deepcopy(lhs), 'RHS': [copy.deepcopy(new_nt), copy.deepcopy(last_el)], 'p': copy.deepcopy(p)})
                    # Prepare for next rule
                    lhs = new_nt
                    p = 1
                cnf.append({'LHS': lhs, 'RHS': [new_rhs[0], new_nt], 'p': p})
                lhs = new_nt
                new_rhs = new_rhs[1:]
            cnf.append({'LHS': lhs, 'RHS': new_rhs, 'p': p})

    for rule in grammar:
        lhs = rule['LHS']
        rhs = rule['RHS']
        p = rule['p']

        if len(rhs) == 1 and (rhs[0] in rules_by_lhs.keys()):
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
    rules_by_lhs = get_non_terminals(cnf)
    for rule in cnf:
        if not (rule['LHS'] in rules_by_lhs):
            print('!' * 20, 'Incorrect(1): ', rule)
        elif len(rule['RHS']) == 1 and (rule['RHS'][0] in rules_by_lhs):
            print('!' * 20, 'Incorrect(2): ', rule)
        elif len(rule['RHS']) == 2 and ((rule['RHS'][0] not in rules_by_lhs) or 
                (rule['RHS'][1] not in rules_by_lhs)):
            print('!' * 20, 'Incorrect(3): ', rule)
    exit(0)
    return cnf


cnf_grammar = convert_to_cnf(contextFreeGrammar)
for rule in cnf_grammar:
    print(f"{rule['LHS']:<15} -> {str(rule['RHS']):<25} (p={rule['p']:<5})")