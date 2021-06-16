import random

def ask_string():
    length = 100
    gen_str = []
    print("Please give AI some data to learn...\nThe current data length is 0, 100 symbols left")
    while True:
        user = input("Print a random string containing 0 or 1:\n")
        gen_str.extend([c for c in user if c in ['0', '1']])
        if len(gen_str) > length:
            break
        print(f"Current data length is {len(gen_str)}, {length - len(gen_str)} symbols left")
    final = ''.join(gen_str)[:length]
    print(f"Final data string:\n{final}")
    return final


def stats(final):
    di = {}
    for i in range(len(final)-3):
        triad = final[i:i+3]
        di.setdefault(triad,[0,0])
        follow = final[i+3]
        if int(follow):
            di[triad][1] += 1
        else:
            di[triad][0] += 1

    order = ['000', '001', '010', '011', '100', '101', '110', '111']
    return {i: [{di.get(i, [0, 0])[0]}, {di.get(i, [0, 0])[1]}] for i in order}


def rdm_triad():
    return ''.join(str(random.randint(0,1)) for _ in range(3))


def ask_test_string():
    user = input("Print a random string containing 0 or 1:\n")
    if user == "enough":
        return False
    elif len([c for c in user if c not in ['0', '1']]) != 0:
        print("some wrong input")
        return 'wrong'
    return user


def prediction(tst):
    print('prediction:')
    rdm_str = []
    for i in range(len(tst)-3):
        tr = tst[i:i+3]
        if list(st[tr][0])[0] > list(st[tr][1])[0]:
            rdm_str.append('0')
        else:
            rdm_str.append('1')
    res = ''.join(rdm_str)
    print(rdm_triad() + res)
    return res


def result(tst, pr):
    n = sum(t == p for t, p in zip(tst[3:], pr))
    m = len(pr)
    res = round(((n/m) * 100), 2)
    print(f'Computer guessed right {n} out of {m} symbols ({res})')
    return (m - n) - n


capital = 1000
final = ask_string()
st = stats(final)
print(f'You have ${capital}. Every time the system successfully predicts your next press, you lose $1.\nOtherwise, you earn $1. Print "enough" to leave the game. Let\'s go!')
while True:
    tst = ask_test_string()
    if not tst:
        print('Game over!')
        break
    if tst is "wrong":
        continue
    pr = prediction(tst)
    capital += result(tst, pr)
    print(f'Your capital is now ${capital}')
    if capital <= 0:
        print('Game over!')
