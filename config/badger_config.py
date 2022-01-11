import json
from dotmap import DotMap
from helpers.eth_registry import registry

curve = registry.curve
pools = registry.curve.pools
convex = registry.convex
whales = registry.whales

sett_config = DotMap(
    native=DotMap(
        convexMimCrv=DotMap(
            strategyName="StrategyConvexStakingOptimizer",
            params=DotMap(
                want=pools.mimCrv.token,
                pid=curve.pids.mimCrv,
                performanceFeeStrategist=0,
                performanceFeeGovernance=2000,
                withdrawalFee=10,
                curvePool=DotMap(
                    swap=registry.curve.pools.mimCrv.swap,
                    usdcPosition=2,
                    numElements=4,
                ),
                cvxHelperVault=convex.cvxHelperVault,
                cvxCrvHelperVault=convex.cvxCrvHelperVault,
            ),
        ),
        convexFraxCrv=DotMap(
            strategyName="StrategyConvexStakingOptimizer",
            params=DotMap(
                want=pools.fraxCrv.token,
                pid=curve.pids.fraxCrv,
                performanceFeeStrategist=0,
                performanceFeeGovernance=2000,
                withdrawalFee=10,
                curvePool=DotMap(
                    swap=registry.curve.pools.fraxCrv.swap,
                    usdcPosition=2,
                    numElements=4,
                ),
                cvxHelperVault=convex.cvxHelperVault,
                cvxCrvHelperVault=convex.cvxCrvHelperVault,
            ),
        ),
    ),
)

badger_config = DotMap(
    prod_json="deploy-final.json",
)

config = DotMap(
    badger=badger_config,
    sett=sett_config,
)
