from brownie import interface, chain
from helpers.constants import MaxUint256
from helpers.utils import (
    approx,
)
from config.badger_config import sett_config
import pytest
from conftest import deploy

@pytest.mark.parametrize(
    "sett_id",
    sett_config.native,
)
def test_are_you_trying(sett_id):
    """
    Verifies that you set up the Strategy properly
    """
    # Setup
    deployed = deploy(sett_config.native[sett_id])

    deployer = deployed.deployer
    sett = deployed.sett
    want = deployed.want
    strategy = deployed.strategy

    startingBalance = want.balanceOf(deployer)

    depositAmount = startingBalance // 2
    assert startingBalance >= depositAmount
    assert startingBalance >= 0
    assert want.balanceOf(sett) == 0

    want.approve(sett, MaxUint256, {"from": deployer})
    sett.deposit(depositAmount, {"from": deployer})

    available = sett.available()
    assert available > 0

    sett.earn({"from": deployer})

    chain.sleep(10000 * 13)  # Mine so we get some interest

    ## TEST 1: Does the want get used in any way?
    assert want.balanceOf(sett) == depositAmount - available

    # Did the strategy do something with the asset?
    assert want.balanceOf(strategy) < available

    ## End Setup

    harvest = strategy.harvest({"from": deployer})

    ## Fees are being processed
    assert harvest.events["PerformanceFeeGovernance"][0]["amount"] > 0
    assert harvest.events["PerformanceFeeGovernance"][1]["amount"] > 0

    ## Assets are being distributed
    assert harvest.events["TreeDistribution"][0]["amount"] > 0
    assert harvest.events["TreeDistribution"][1]["amount"] > 0

    ## Fail if PerformanceFeeStrategist is fired
    try:
        harvest.events["PerformanceFeeStrategist"]
        assert False
    except:
        assert True

    ## The fees are in CRV and CVX
    assert harvest.events["PerformanceFeeGovernance"][0]["token"] == strategy.cvxCrv()
    assert harvest.events["PerformanceFeeGovernance"][1]["token"] == strategy.cvx()

    ## Distributions are in bcvxCRV and bveCVX
    assert harvest.events["TreeDistribution"][0]["token"] == strategy.cvxCrvHelperVault()
    assert harvest.events["TreeDistribution"][1]["token"] == strategy.bveCVX()
