// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IBorrowerOperations} from "../../src/interfaces/IBorrowerOperations.sol";
import {MockMUSD} from "./MockMUSD.sol";
import {MockTroveManager} from "./MockTroveManager.sol";

/// @notice Test double for Mezo BorrowerOperations.
/// @dev    Simulates the state mutations openTrove / addColl / repay /
///         closeTrove perform on the real contract: minting MUSD to the
///         caller, recording debt + coll on a stand-in TroveManager.
contract MockBorrowerOperations is IBorrowerOperations {
    MockMUSD public immutable musd;
    MockTroveManager public immutable troveManager;

    constructor(MockMUSD _musd, MockTroveManager _troveManager) {
        musd = _musd;
        troveManager = _troveManager;
    }

    function openTrove(
        uint256 /* _maxFeePercentage */,
        uint256 _MUSDAmount,
        uint256 /* _interestRate */,
        address /* _upperHint */,
        address /* _lowerHint */
    ) external payable override {
        troveManager.setTrove(msg.sender, _MUSDAmount, msg.value, 1);
        musd.mint(msg.sender, _MUSDAmount);
    }

    function addColl(address, address) external payable override {
        troveManager.addColl(msg.sender, msg.value);
    }

    function withdrawColl(uint256 _collWithdrawal, address, address) external override {
        troveManager.removeColl(msg.sender, _collWithdrawal);
        (bool ok, ) = msg.sender.call{value: _collWithdrawal}("");
        require(ok, "btc refund failed");
    }

    function withdrawMUSD(
        uint256,
        uint256 _MUSDAmount,
        address,
        address
    ) external override {
        troveManager.addDebt(msg.sender, _MUSDAmount);
        musd.mint(msg.sender, _MUSDAmount);
    }

    function repayMUSD(uint256 _MUSDAmount, address, address) external override {
        musd.burn(msg.sender, _MUSDAmount);
        troveManager.removeDebt(msg.sender, _MUSDAmount);
    }

    function closeTrove() external override {
        (uint256 debt, uint256 coll) = troveManager.snapshot(msg.sender);
        if (debt > 0) {
            musd.burn(msg.sender, debt);
        }
        troveManager.clearTrove(msg.sender);
        if (coll > 0) {
            (bool ok, ) = msg.sender.call{value: coll}("");
            require(ok, "btc refund failed");
        }
    }

    function adjustTrove(
        uint256,
        uint256 _collWithdrawal,
        uint256 _MUSDChange,
        bool _isDebtIncrease,
        address,
        address
    ) external payable override {
        if (msg.value > 0) troveManager.addColl(msg.sender, msg.value);
        if (_collWithdrawal > 0) {
            troveManager.removeColl(msg.sender, _collWithdrawal);
            (bool ok, ) = msg.sender.call{value: _collWithdrawal}("");
            require(ok, "btc refund failed");
        }
        if (_MUSDChange > 0) {
            if (_isDebtIncrease) {
                troveManager.addDebt(msg.sender, _MUSDChange);
                musd.mint(msg.sender, _MUSDChange);
            } else {
                musd.burn(msg.sender, _MUSDChange);
                troveManager.removeDebt(msg.sender, _MUSDChange);
            }
        }
    }

    receive() external payable {}
}
