// SPDX-License-Identifier: MIT
pragma solidity >=0.5.0 <0.8.0;

interface ISettV4 {
    function token() external view returns (address);

    function decimals() external view returns (uint256);

    function keeper() external view returns (address);

    function governance() external view returns (address);

    function deposit(uint256) external;

    function setController(address) external;

    function depositFor(address, uint256) external;

    function depositAll() external;

    function withdraw(uint256) external;

    function withdrawAll() external;

    function earn() external;

    function balanceOf(address account) external view returns (uint256);

    function totalSupply() external view returns (uint256);

    function balance() external view returns (uint256);

    function claimInsurance() external; // NOTE: Only yDelegatedVault implements this

    function getPricePerFullShare() external view returns (uint256);
}
