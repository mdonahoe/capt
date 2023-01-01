from collections import defaultdict


HEALTH = 'health'
ENERGY = 'energy'
FOOD = 'food'


def create_man():
    man = defaultdict(int)
    man[HEALTH] = 50
    man[ENERGY] = 100
    return man


def explore_blocker(man):
    if man[FOOD] > 99: return FOOD
    if man[ENERGY] < 10: return ENERGY
    return ''


def do_explore(man):
    man[ENERGY] -= 1
    man[FOOD] += 1
    return man


def do_rest(man):
    man[HEALTH] -= 1
    man[ENERGY] += 100
    return man


def rest_blocker(man):
    if man[ENERGY] > 99: return ENERGY
    if man[HEALTH] < 1: return HEALTH
    return ''


def rest(man):
    blocker = rest_blocker(man)
    if blocker:
        print('cant rest because', blocker)
        return man
    return do_rest(man)


def explore(man):
    blocker = explore_blocker(man)
    if blocker:
        print('cant explore because', blocker)
        return man
    return do_explore(man)


def eat_blocker(man):
    if man[FOOD] < 1: return FOOD
    if man[HEALTH] > 99: return HEALTH
    return ''


def do_eat(man):
    man[FOOD] -= 1
    man[HEALTH] += 10
    return man


def eat(man):
    blocker = eat_blocker(man)
    if blocker:
        print('cant eat because', blocker)
        return man
    return do_eat(man)


actions = [
    ('eat', eat_blocker, eat),
    ('rest', rest_blocker, rest), 
    ('explore', explore_blocker, explore),
]

resources = [
    HEALTH,
    ENERGY,
    FOOD,
]


def loop(townsfolk):
    while True:
        for r in resources:
            row = [r]
            for f in townsfolk:
                row.append(str(f[r]))
            print(', '.join(row))
        act_map = {}
        for act_name, act_blocker, act_func, in actions:
            num_can_act = 0
            for f in townsfolk:
                if not act_blocker(f):
                    num_can_act += 1
            if num_can_act > 0:
                print("{} ({})".format(act_name, num_can_act))
                act_map[act_name] = act_func
        while True:
            act = raw_input('>>> ')
            if act in act_map:
                break
            else:
                print('invalid action {}. expected {}'.format(act, ', '.join(act_map.keys())))
        action = act_map[act]
        for f in townsfolk:
            action(f)

loop([create_man()])
