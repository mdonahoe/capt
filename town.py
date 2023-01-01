from collections import defaultdict
from random import randint


HEALTH = 'health'
ENERGY = 'energy'
FOOD = 'food'
THREAT = 'threat'

EXPLORING_SKILL = 'explorer'
FIGHTING_SKILL = 'fighter'


def create_man():
    man = defaultdict(int)
    man[HEALTH] = 50
    man[ENERGY] = 100
    man[EXPLORING_SKILL] = randint(1, 20)
    man[FIGHTING_SKILL] = randint(1, 20)
    return man


def explore_blocker(man):
    if man[HEALTH] < 1: return HEALTH
    if man[FOOD] > 99: return FOOD
    if man[ENERGY] < 20: return ENERGY
    if man[THREAT] > max(0, 20 - man[EXPLORING_SKILL]): return THREAT
    return ''


def do_explore(man):
    man[ENERGY] -= 20
    man[FOOD] += 2 * man[EXPLORING_SKILL]
    if man[EXPLORING_SKILL] == 20:
        man[THREAT] += 1
    elif man[EXPLORING_SKILL] == 1:
        man[THREAT] += 100
    elif man[EXPLORING_SKILL] > 15:
        man[THREAT] += 5
    elif man[EXPLORING_SKILL] < 5:
        man[THREAT] += 50
    else:
        man[THREAT] += 20
    return [man]


def do_rest(man):
    man[HEALTH] -= 1
    man[ENERGY] += 5
    return [man]


def rest_blocker(man):
    if man[ENERGY] > 99: return ENERGY
    if man[HEALTH] < 1: return HEALTH
    if man[THREAT] > 0: return THREAT
    return ''


def rest(man):
    blocker = rest_blocker(man)
    if blocker:
        #print('cant rest because', blocker)
        return [man]
    return do_rest(man)


def explore(man):
    blocker = explore_blocker(man)
    if blocker:
        #print('cant explore because', blocker)
        return [man]
    return do_explore(man)


def eat_blocker(man):
    if man[FOOD] < 1: return FOOD
    if man[HEALTH] > 99: return HEALTH
    if man[THREAT] > 1: return THREAT
    return ''

def do_eat(man):
    man[FOOD] -= 1
    man[HEALTH] += 1
    return [man]

def eat(man):
    blocker = eat_blocker(man)
    if blocker:
        #print('cant eat because', blocker)
        return [man]
    return do_eat(man)

def reproduce_blocker(man):
    if man[HEALTH] <= 99: return HEALTH
    if man[THREAT] > 0: return THREAT
    if man[ENERGY] < 50: return ENERGY
    return ''

def do_reproduce(man):
    m1 = create_man()
    m2 = create_man()
    for key, val in man.items():
        half = int(val / 2)
        m1[key] = half
        m2[key] = half

    # man keeps original skill
    m1[EXPLORING_SKILL] = man[EXPLORING_SKILL]
    m1[FIGHTING_SKILL] = man[FIGHTING_SKILL]

    # new man gets random skill
    # TODO: genetics
    m2[EXPLORING_SKILL] = randint(1, 20)
    m2[FIGHTING_SKILL] = randint(1, 20)
    return [m1, m2]


def reproduce(man):
    blocker = reproduce_blocker(man)
    if blocker:
        #print('cant reproduce because', blocker)
        return [man]
    return do_reproduce(man)

def fight_blocker(man):
    if man[THREAT] < 1: return THREAT
    if man[HEALTH] < 1: return HEALTH
    # energy is not required to fight, but you'll probably lose
    return ''


def do_fight(man):
    if man[ENERGY] > 0:
        man[THREAT] -= 2 * man[FIGHTING_SKILL]
        man[ENERGY] -= 20
    else:
        man[THREAT] -= 1

    # if there is still a threat, lose health
    if man[THREAT] > 0 or man[FIGHTING_SKILL] < 10:
        man[HEALTH] -= 25
    else:
        # TODO:negative could be interesting to try, with limits
        man[THREAT] = 0
    return [man]


def fight(man):
    blocker = fight_blocker(man)
    if blocker:
        #print('cant fight because', blocker)
        return [man]
    return do_fight(man)


def die_blocker(man):
    if man[HEALTH] > 0: return HEALTH
    return ''

def do_die(man):
    # TODO: distribute food and skills?
    return []

def die(man):
    blocker = die_blocker(man)
    if blocker:
        #print('cant die because', blocker)
        return [man]
    return do_die(man)


actions = [
    ('eat', eat_blocker, eat),
    ('rest', rest_blocker, rest), 
    ('explore', explore_blocker, explore),
    ('reproduce', reproduce_blocker, reproduce),
    ('fight', fight_blocker, fight),
    ('die', die_blocker, die),
]

blocker_map = dict((act, blocker) for (act, blocker, _) in actions)

resources = [
    HEALTH,
    ENERGY,
    FOOD,
    THREAT,
]

skills = [
    EXPLORING_SKILL,
    FIGHTING_SKILL,
]


def input_actions(act_map):
    while True:
        acts = raw_input('>>> ').split()
        for act in act_map:
            if act in act_map:
                return acts
        else:
            print('invalid actions {}. expected one of {}'.format(acts, ', '.join(act_map.keys())))

def loop(townsfolk):
    while len(townsfolk):
        print('RESOURCES:')
        for r in resources:
            row = [r]
            minr = min(f[r] for f in townsfolk)
            maxr = max(f[r] for f in townsfolk)
            if len(townsfolk) > 0:
                mean = sum(f[r] for f in townsfolk) / len(townsfolk)
            else:
                mean = 0
            print(r, minr, mean, maxr)

        print('\nSKILLS:')
        for r in skills:
            row = [r]
            minr = min(f[r] for f in townsfolk)
            maxr = max(f[r] for f in townsfolk)
            if len(townsfolk) > 0:
                mean = sum(f[r] for f in townsfolk) / len(townsfolk)
            else:
                mean = 0
            print(r, minr, mean, maxr)

        print('\nACTIONS:')
        act_map = {}
        for act_name, act_blocker, act_func, in actions:
            num_can_act = 0
            for f in townsfolk:
                if not act_blocker(f):
                    num_can_act += 1
            if num_can_act > 0:
                act_map[act_name] = act_func
                print("{} ({})".format(act_name, num_can_act))

        acts = input_actions(act_map)
        num_loops = 300
        while num_loops > 0:
            num_loops -= 1
            did_any = False
            for act in acts:

                act_map = {}
                for act_name, act_blocker, act_func, in actions:
                    num_can_act = 0
                    for f in townsfolk:
                        if not act_blocker(f):
                            num_can_act += 1
                    if num_can_act > 0:
                        act_map[act_name] = act_func

                if act not in act_map:
                    print(act, "not in ", act_map)
                    continue
                did_any = True

                action = act_map[act]
                num_rounds = 0
                num_can = 1
                num_actors = 0
                start_size = len(townsfolk)
                while num_can > 0:
                    new_town = []
                    for f in townsfolk:
                        new_town.extend(action(f))
                    num_rounds += 1
                    townsfolk = new_town
                    num_can = 0
                    for f in townsfolk:
                        if blocker_map[act](f):
                            pass
                        else:
                            num_can += 1
                print('{} performed {} for {} rounds'.format(start_size, act, num_rounds))
            if did_any is False:
                break
        print('Your town is now {} people'.format(len(townsfolk)))
    if len(townsfolk):
        print('congrats')
    else:
        print('your town has died.')

loop([create_man() for _ in range(10)])
