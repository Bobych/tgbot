def weiToUsdt(wei):
    usdt = float(wei) * (10 ** -18)
    result = f"{usdt:.{5}}"
    return result

def gweiToUsdt(wei):
    usdt = float(wei) * (10 ** -9)
    result = f"{usdt:.{5}}"
    return result