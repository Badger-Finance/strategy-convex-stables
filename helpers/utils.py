from config.badger_config import sett_config

# Assert approximate integer
def approx(actual, expected, percentage_threshold):
    print(actual, expected, percentage_threshold)
    diff = int(abs(actual - expected))
    # 0 diff should automtically be a match
    if diff == 0:
        return True
    return diff < (actual * percentage_threshold // 100)


def val(amount=0, decimals=18, token=None):
    # return amount
    # return "{:,.0f}".format(amount)
    # If no token specified, use decimals
    if token:
        decimals = interface.IERC20(token).decimals()

    return "{:,.18f}".format(amount / 10 ** decimals)

def get_config(strategy_key):
    if strategy_key == "native.mimCrv":
        return sett_config.native.convexMimCrv
    if strategy_key == "native.fraxCrv":
        return sett_config.native.convexFraxCrv
