import math


def power_gen(area, eff, irrad, sysloss, cf, b, a, y):
    return area * eff * irrad * sysloss * cf * math.cos(b * math.pi / 180) * math.cos((a - y) * math.pi / 180)
