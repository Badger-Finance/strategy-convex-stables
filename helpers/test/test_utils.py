from brownie import interface
import time
from rich.console import Console
from helpers.constants import SUSHI_ROUTER, MaxUint256
from helpers.eth_registry import registry

console = Console()
tokens = registry.tokens
curve = registry.curve

def generate_test_assets(account, path, amount):
    console.print("[yellow]Swapping for test assets...[/yellow]")
    # Using Sushiswap router
    router = interface.IUniswapRouterV2(SUSHI_ROUTER)

    for address in path:
        asset = interface.IERC20(address)
        asset.approve(router.address, MaxUint256, {"from": account})

    # Buy path[n-1] token with "amount" of path[0] token
    router.swapExactETHForTokens(
        0,
        path,
        account,
        int(time.time()) + 120000000, # Add some time so tests don't fail,
        {"from": account, "value": amount}
    )

    console.print("[green]Test assets acquired![/green]")

def generate_curve_LP_assets(account, amount, sett_config):
    console.print("[yellow]Depositing for LP tokens...[/yellow]")

    poolInfo = sett_config.params.curvePool

    # Generate usdc
    path = [tokens.weth, tokens.usdc]
    generate_test_assets(account, path, amount)
    usdc = interface.IERC20(tokens.usdc)
    usdcAmount = usdc.balanceOf(account.address)

    zap = interface.ICurveZapIbBTC(curve.crvUSDZap) # Function has the same signature
    usdc.approve(zap.address, MaxUint256, {"from": account})

    amounts = [0] * poolInfo.numElements
    amounts[poolInfo.usdcPosition] = usdcAmount
    zap.add_liquidity(
        sett_config.params.want, # MIM or FRAX Crv pool
        amounts,
        0,
        account.address,
        {"from": account}
    )

    console.print("[green]Test LP tokens acquired![/green]")