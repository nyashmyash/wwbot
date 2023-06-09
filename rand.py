import random

def randint(start: int, end: int, use_gauss = False) -> int:
    if not use_gauss:
        return random.randint(start, end)
        r = end - start
        if round(r/2) == 0:
            return random.randint(start, end)

        r1 = random.randint(0, round(r/2))
        r2 = random.randint(round(r / 2), r)
        if randint(0, 1) == 1:
            return r2
        else:
            return r1

    mu = 2
    sigma = 0.8
    k = 0
    max = 0
    rlist = []
    while k < 100:
        rnd_num = abs(random.gauss(mu, sigma))
        if rnd_num > max:
            max = rnd_num
        rlist.append(rnd_num)
        k += 1
    val = random.choice(rlist)/max
    return start + round((end - start)*val)
