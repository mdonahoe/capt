from collections import defaultdict
from random import randint


HEALTH = 'health'
ENERGY = 'energy'
FOOD = 'food'
THREAT = 'threat'
CLOTHES = 'clothes'
TOOLS = 'tools'
HAPPINESS = 'happy'

EXPLORING_SKILL = 'explorer'
FIGHTING_SKILL = 'fighter'


"""

Problems:
1. Lots of people die after the first exploration.
2. What's the goal? Last 365 days?
3. Reproduction happens too quickly.
4. Bad decisions don't lead to deaths.
5. Everyone is independent. No sharing, mating, teaching, etc.


"""


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
    else:
        man[THREAT] += 20
    man[HAPPINESS] -= man[THREAT]
    if man[HAPPINESS] < 0:
        man[HAPPINESS] = 0
    return [man]


def do_rest(man):
    man[HEALTH] -= 1
    man[ENERGY] += max(1, man[CLOTHES])
    if man[ENERGY] > 99:
        man[ENERGY] = 100
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
    if man[THREAT] > 0: return THREAT
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
    if man[HAPPINESS] <= 99: return HAPPINESS
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
    if man[THREAT] < 0:
        man[THREAT] = 0

    # if there is still a threat, lose health
    if man[THREAT] > 0 or man[FIGHTING_SKILL] < 10:
        damage = 45
    else:
        damage = 0

    if man[CLOTHES] > damage:
        man[CLOTHES] -= damage
    elif man[CLOTHES] > 0:
        damage -= man[CLOTHES]
        man[CLOTHES] = 0

    man[HEALTH] -= damage

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

def sew_blocker(man):
    if man[THREAT] > 0: return THREAT
    if man[HEALTH] < 1: return HEALTH
    if man[ENERGY] < 10: return ENERGY
    if man[CLOTHES] > 99: return CLOTHES
    return ''

def do_sew(man):
    man[CLOTHES] += 1
    man[ENERGY] -= 10
    return [man]

def sew(man):
    blocker = sew_blocker(man)
    if blocker:
        return [man]
    return do_sew(man)

def party_blocker(man):
    if man[HEALTH] < 50: return HEALTH
    if man[ENERGY] < 1: return HEALTH
    if man[THREAT] > 0: return HEALTH
    if man[HAPPINESS] > 99: return HAPPINESS
    return ''

def do_party(man):
    man[HAPPINESS] += 1
    man[ENERGY] -= 1
    return [man]

def party(man):
    blocker = party_blocker(man)
    if blocker:
        return [man]
    return do_party(man)


ACTIONS = [
    ('eat', eat_blocker, eat),
    ('rest', rest_blocker, rest), 
    ('explore', explore_blocker, explore),
    ('reproduce', reproduce_blocker, reproduce),
    ('fight', fight_blocker, fight),
    ('die', die_blocker, die),
    ('sew', sew_blocker, sew),
    ('party', party_blocker, party),
]

blocker_map = dict((act, blocker) for (act, blocker, _) in ACTIONS)

RESOURCES = [
    HEALTH,
    ENERGY,
    FOOD,
    CLOTHES,
    HAPPINESS,
    THREAT,
]

SKILLS = [
    EXPLORING_SKILL,
    FIGHTING_SKILL,
]


def input_actions():
    acts = input('>>> ').split()
    return acts

def print_stats(townsfolk):
    print('RESOURCES:')
    for r in RESOURCES:
        row = [r]
        minr = min(f[r] for f in townsfolk)
        maxr = max(f[r] for f in townsfolk)
        if len(townsfolk) > 0:
            mean = sum(f[r] for f in townsfolk) / len(townsfolk)
        else:
            mean = 0
        print(r, minr, mean, maxr)

    print('\nSKILLS:')
    for r in SKILLS:
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
    for act_name, act_blocker, act_func, in ACTIONS:
        num_can_act = 0
        for f in townsfolk:
            if not act_blocker(f):
                num_can_act += 1
        if num_can_act > 0:
            act_map[act_name] = act_func
            print("{} ({})".format(act_name, num_can_act))


def eval_actions(acts, townsfolk, max_loops=300):
    num_loops = max_loops
    while num_loops > 0:
        num_loops -= 1
        did_any = False
        for act in acts:

            act_map = {}
            for act_name, act_blocker, act_func, in ACTIONS:
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
    return townsfolk


def main(townsfolk):
    while len(townsfolk):
        print_stats(townsfolk)
        acts = input_actions()
        townsfolk = eval_actions(acts, townsfolk)
        print('Your town is now {} people'.format(len(townsfolk)))
    if len(townsfolk):
        print('congrats')
    else:
        print('your town has died.')


if __name__ == '__main__':
    starting_town_size = 10
    main([create_man() for _ in range(starting_town_size)])
