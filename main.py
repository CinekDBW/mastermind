import constant
import random
from collections import Counter

ALL_POSSIBILITIES = []
ALL = []
ALL_COPY = []
ELITE = []
POSSIBLE_SCORES = []


def randomPattern():
    pattern = []
    for i in range(0, constant.SLOTS):
        pattern.append(random.randint(0, constant.COLORS - 1))
    return pattern


def guessPattern(guess, pattern):
    on_position = 0  # tells that particular color is guessed on proper position
    exists = 0  # tells that particular color exists in the original pattern, but on different position

    guess_copy = []
    pattern_copy = []

    for i in range(len(guess)):
        if guess[i] != pattern[i]:
            guess_copy.append(guess[i])
            pattern_copy.append(pattern[i])
        else:
            on_position += 1

    guess_occurences = Counter(guess_copy)
    pattern_occurences = Counter(pattern_copy)

    for g in guess_occurences:
        exists += min(guess_occurences[g], pattern_occurences[g])

    return on_position, exists


def play(mode, original_pattern=randomPattern(), is_silent=True):
    init_play()
    if not is_silent:
        print("HASLO: ", original_pattern)

    score = (0, 0)
    score_list = []
    guess_list = []
    counter = 0
    while score[0] != constant.SLOTS:
        counter += 1
        shot = mode(guess_list, score_list)
        score = guessPattern(shot, original_pattern)
        guess_list.insert(0, shot)
        score_list.insert(0, score)
    if not is_silent:
        print("Twoj wynik to: ", counter)
    return counter


def play_gui(mode):
    init_play()
    original_pattern = randomPattern()

    score = (0, 0)
    score_list = []
    guess_list = []
    counter = 0
    while score[0] != constant.SLOTS:
        counter += 1
        shot = mode(guess_list, score_list)
        score = guessPattern(shot, original_pattern)
        guess_list.insert(0, shot)
        score_list.insert(0, score)
    return guess_list, score_list, original_pattern




def manually(previous_guess, previous_scores):
    my_list = []

    print(previous_scores)
    print(previous_guess)

    for i in range(0, constant.SLOTS):
        var = input("Podaj kolor %d " % i)
        my_list.append(int(var))
    return my_list


def rng(previous_guess, previous_scores):
    my_list = randomPattern()
    while (my_list in previous_guess):
        my_list = randomPattern()
    return my_list

def dummy(previous_guess, previous_scores):

    my_list = ALL_POSSIBILITIES[len(previous_guess)]

    return my_list

def minimax(prev_guess):
    curr_score = []

    for item in ALL_POSSIBILITIES:
        if item not in prev_guess:
            hitMap = [0] * len(POSSIBLE_SCORES)
            for ac in ALL_COPY:
                hitMap[POSSIBLE_SCORES.index(guessPattern(ac, item))] += 1
            curr_score.append(len(ALL_COPY) - max(hitMap))
        else:
            curr_score.append(0)

    max_score = max(curr_score)
    max_score_indexes = [i for i, x in enumerate(curr_score) if x == max_score]

    guess = ALL_POSSIBILITIES[max_score_indexes[0]]
    for i in range(len(max_score_indexes)):
        if ALL_POSSIBILITIES[max_score_indexes[i]] in ALL_COPY:
            guess = ALL_POSSIBILITIES[max_score_indexes[i]]
            break

    return guess


def knuth(previous_guess, previous_scores):
    global ALL, ALL_COPY
    if not previous_guess:
        quotient = int(constant.SLOTS / 2)
        my_list = [0] * quotient + [1] * (constant.SLOTS - quotient)
    else:
        for case in ALL:
            if previous_scores[0] != guessPattern(case, previous_guess[0]):
                # print("usuwam ", case)
                ALL_COPY.remove(case)
        # print(ALL_COPY)
        my_list = minimax(previous_guess)
        ALL = ALL_COPY.copy()
    return my_list


def init_pop(prev_guess, prev_scores):
    population = []
    indexes = []
    indexes = random.sample(range(constant.COLORS ** constant.SLOTS), constant.POPULATION_SIZE)
    for i in indexes:
        if ALL[i] not in prev_guess :
            population.append((ALL[i], calc_fitness(ALL[i], prev_guess, prev_scores)))
    # print(population)
    return population


def inversion(pattern):
    if random.random() <= 0.02:
        # print("INWERSJA")
        index1 = random.randint(0, constant.SLOTS - 1)
        index2 = index1
        while index2 == index1:
            index2 = random.randint(0, constant.SLOTS - 1)
        if index1 > index2:
            index1, index2 = index2, index1

        pattern[index1:index2 + 1] = pattern[index1:index2 + 1][::-1]


def permutation(pattern):
    if random.random() <= 0.03:
        index1 = random.randint(0, constant.SLOTS - 1)
        index2 = random.randint(0, constant.SLOTS - 1)
        # print("PERMUTACJA", )
        pattern[index1], pattern[index2] = pattern[index2], pattern[index1]


def mutation(pattern):
    if random.random() <= 0.03:
        # print("MUTACJA")
        pattern[random.randint(0, constant.SLOTS - 1)] = random.randint(0, constant.COLORS - 1)


def crossover(parent1, parent2):
    p1 = parent1.copy()
    p2 = parent2.copy()
    rand = random.randint(1, 2)
    if (rand == 1):  # 1-point crossover
        pivot = random.randint(1, constant.SLOTS - 1)
        for i in range(0, pivot):
            p1[i], p2[i] = p2[i], p1[i]
    else:  # 2-point crossover
        pivot1 = random.randint(1, constant.SLOTS - 2)
        pivot2 = random.randint(pivot1 + 1, constant.SLOTS - 1)
        for i in range(pivot1, pivot2):
            p1[i], p2[i] = p2[i], p1[i]
    return p1, p2


def new_population(population, prev_guess, prev_scores):
    pop = population[0:int(len(population) / 2)]
    # print(pop)
    for i in range(0, len(pop), 2):
        current_guess1 = pop[i][0]
        current_guess2 = pop[i + 1][0]
        new1, new2 = crossover(current_guess1, current_guess2)
        mutation(new1)
        mutation(new2)
        permutation(new1)
        permutation(new2)
        inversion(new1)
        inversion(new2)
        # print("fitness rodzicow: ", pop[i],"      ", pop[i+1], "     ", new1, "                ", calc_fitness(new1, prev_guess, prev_scores))
        pop.append((new1, calc_fitness(new1, prev_guess, prev_scores)))
        pop.append((new2, calc_fitness(new2, prev_guess, prev_scores)))
    # print(len(pop) ,"    " , pop)
    return pop


def genetic(previous_guess, previous_scores):
    i = 1
    if not previous_guess:
        my_list = [0, 0, 1, 2]
    else:
        while (previous_scores[0] != (4, 0)):
            i += 1
            h = 1

            # Init population
            population = init_pop(previous_guess, previous_scores)
            global ELITE
            for el in ELITE:
                population.append(el)

            c = 0
            while (h <= constant.MAX_GEN):
                h += 1
                population.sort(key=lambda t: t[1], reverse=True)
                population = new_population(population, previous_guess, previous_scores)
                population.sort(key=lambda t: t[1], reverse=True)

                ELITE = []

                for i in range(10):
                    if population[i][1] > 10:
                        ELITE.append(population[i])
                # print("EKITE: ", ELITE)
                # print(population[0])
            my_list = population[0][0]
            index = 0
            while my_list in previous_guess:
                index+=1
                my_list = population[index][0]
            return my_list
    return my_list


def calc_fitness(current, prev_guess, prev_scores):
    fitness = 0
    for i in range(len(prev_guess)):
        if current == prev_guess[i]:
            return 0
        if prev_scores[i] != guessPattern(current, prev_guess[i]):
            return 0
        else:
            fitness += 10
    return fitness


def smart_random(previous_guess, previous_scores):
    global ALL
    if previous_guess:
        for case in ALL:
            if previous_scores[0] != guessPattern(case, previous_guess[0]):
                ALL_COPY.remove(case)
        ALL = ALL_COPY.copy()
    my_list = ALL_COPY[random.randint(0, len(ALL_COPY) - 1)]
    return my_list


def init_play():
    global ALL, ALL_COPY, ELITE
    ELITE = []

    ALL = ALL_POSSIBILITIES.copy()
    ALL_COPY = ALL_POSSIBILITIES.copy()


def calc_avg(mode):
    counter = 0
    for i in range(0, constant.AVERAGE_COUNT):
        counter += play(mode, ALL_POSSIBILITIES[i])
    return counter / constant.AVERAGE_COUNT


def init_all():
    global POSSIBLE_SCORES, ALL_POSSIBILITIES
    for i in range(0, constant.SLOTS):
        for j in range(0, constant.SLOTS - i + 1):
            if i != constant.SLOTS - 1 or j != 1:
                POSSIBLE_SCORES.append((i, j))
    POSSIBLE_SCORES.append((constant.SLOTS, 0))

    my_list = [0] * constant.SLOTS
    for i in range(constant.COLORS ** constant.SLOTS):
        ALL_POSSIBILITIES.append(my_list)
        my_list = my_list.copy()
        my_list[-1] += 1
        for i in range(constant.SLOTS - 1, 0, -1):
            if my_list[i] > constant.COLORS - 1:
                my_list[i - 1] += 1
                my_list[i] = 0


if __name__ == '__main__':
    init_all()

    #print("Knuth ", calc_avg(knuth))
    print("Genetic ", calc_avg(genetic))
    #print("Smart random ", calc_avg(smart_random))
    #print("Random ", calc_avg(rng))
    #print("Dummy ", calc_avg(dummy))
