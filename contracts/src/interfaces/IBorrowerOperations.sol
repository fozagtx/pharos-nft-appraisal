// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @notice Subset of Mezo's BorrowerOperations (Liquity-v2 fork) used by AuraVault.
/// @dev Source: github.com/mezo-org/musd. Exact ABI must be cross-checked against
///      the deployed contract on Mezo testnet before mainnet integration.
interface IBorrowerOperations {
    function openTrove(
        uint256 _maxFeePercentage,
        uint256 _MUSDAmount,
        uint256 _interestRate,
        address _upperHint,
        address _lowerHint
    ) external payable;

    function addColl(address _upperHint, address _lowerHint) external payable;

    function withdrawColl(
        uint256 _collWithdrawal,
        address _upperHint,
        address _lowerHint
    ) external;

    function withdrawMUSD(
        uint256 _maxFeePercentage,
        uint256 _MUSDAmount,
        address _upperHint,
        address _lowerHint
    ) external;

    function repayMUSD(
        uint256 _MUSDAmount,
        address _upperHint,
        address _lowerHint
    ) external;

    function closeTrove() external;

    function adjustTrove(
        uint256 _maxFeePercentage,
        uint256 _collWithdrawal,
        uint256 _MUSDChange,
        bool _isDebtIncrease,
        address _upperHint,
        address _lowerHint
    ) external payable;
}
