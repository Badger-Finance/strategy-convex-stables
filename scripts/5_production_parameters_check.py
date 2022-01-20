from brownie import Controller, BadgerRegistry, StrategyConvexStables, SettV4, web3
from config import REGISTRY
from helpers.constants import AddressZero
from helpers.utils import get_config
from rich.console import Console

console = Console()

STRAT_KEYS = [
    "native.mimCrv",
    "native.fraxCrv",
]

STRATEGIES = {
    "native.mimCrv": "0x6D1de7B7F586f17d573BB57ce39159ff6245A285",
    "native.fraxCrv": "0xf1e6aB438136D391fdafff5263f129d434BC6efB",
}

VAULTS = {
    "native.mimCrv": "0x19E4d89e0cB807ea21B8CEF02df5eAA99A110dA5",
    "native.fraxCrv": "0x15cBC4ac1e81c97667780fE6DAdeDd04a6EEB47B",
}

ADMIN_SLOT = "0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103"

def main():
    """
    TO BE RUN BEFORE PROMOTING TO PROD

    Checks the parameters of all of the strategies listed above.
    """

    for key in STRAT_KEYS:

        strategy = StrategyConvexStables.at(STRATEGIES[key])
        controller = Controller.at("0x3F61344BA56df00dad9bBcA05d98CA2AeC43Ba0B")
        vault = SettV4.at(VAULTS[key])

        assert strategy.paused() == False

        console.print(f"[blue]Checking {key}[/blue]")
        console.print("Strategy:", strategy.address)
        console.print("Vault:", vault.address)
        console.print("Controller:", controller.address)
        console.print("Want:", strategy.want())

        # Get production addresses from registry
        registry = BadgerRegistry.at(REGISTRY)

        governance = registry.get("governance")
        treasuryVault = registry.get("treasuryVault")
        guardian = registry.get("guardian")
        keeper = registry.get("keeper")
        badgerTree = registry.get("badgerTree")
        recovered = "0x9faA327AAF1b564B569Cb0Bc0FDAA87052e8d92c"
        devProxyAdmin = registry.get("proxyAdminTimelock")

        assert governance != AddressZero
        assert guardian != AddressZero
        assert keeper != AddressZero
        assert badgerTree != AddressZero
        assert controller != AddressZero
        assert treasuryVault != AddressZero
        assert devProxyAdmin != AddressZero

        # Confirm all productions parameters
        check_parameters(
            governance,
            recovered, 
            guardian, 
            keeper,  
            badgerTree,
            treasuryVault,
            strategy, 
            controller,
            vault,
            key
        )

        # Check that all proxyAdmins match devProxyAdmin
        check_proxyAdmins(
            strategy, 
            controller,
            vault,
            devProxyAdmin
        )


def check_parameters(
    governance,
    recovered, 
    guardian, 
    keeper,  
    badgerTree,
    treasuryVault,
    strategy, 
    controller,
    vault,
    key
):
    config = get_config(key)

    # Check strategy params
    assert strategy.want() == config.params.want

    assert strategy.performanceFeeGovernance() == 0
    assert strategy.performanceFeeStrategist() == 2000
    assert strategy.withdrawalFee() == 10
    assert strategy.stableSwapSlippageTolerance() == 500
    assert strategy.minThreeCrvHarvest() == 1000e18

    assert strategy.keeper() == keeper
    assert strategy.guardian() == guardian
    assert strategy.strategist() == recovered
    assert strategy.governance() == governance

    assert strategy.pid() == config.params.pid
    assert strategy.cvxCrvHelperVault() == config.params.cvxCrvHelperVault
    assert strategy.badgerTree() == badgerTree

    # Check controller params
    assert controller.rewards() == treasuryVault
    assert controller.governance() == governance
    assert controller.strategist() == governance
    assert controller.keeper() == keeper

    # Check vault params
    assert vault.token() == config.params.want
    assert vault.keeper() == keeper
    assert vault.guardian() == guardian
    assert vault.governance() == governance

    # Check proper wire-up
    assert strategy.controller() == controller.address
    assert vault.controller() == controller.address
    assert controller.vaults(config.params.want) == vault.address
    assert controller.strategies(config.params.want) == strategy.address

    console.print("[green]All Parameters checked![/green]")


def check_proxyAdmins(
    strategy, 
    controller,
    vault,
    devProxyAdmin
):
    assert web3.eth.getStorageAt(
        strategy.address, 
        ADMIN_SLOT
        ).hex() == devProxyAdmin
    assert web3.eth.getStorageAt(
        vault.address, 
        ADMIN_SLOT
        ).hex() == devProxyAdmin
    assert web3.eth.getStorageAt(
        controller.address, 
        ADMIN_SLOT
        ).hex() == devProxyAdmin

    console.print("[green]All ProxyAdmins checked![/green]")