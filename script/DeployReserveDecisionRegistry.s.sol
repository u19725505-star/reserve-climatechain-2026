// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {Script, console2} from "forge-std/Script.sol";
import {ReserveDecisionRegistry} from "../contracts/ReserveDecisionRegistry.sol";

contract DeployReserveDecisionRegistry is Script {
    function run() external returns (ReserveDecisionRegistry deployed) {
        require(block.chainid == 11155111, "Sepolia chain ID 11155111 required");
        uint256 deployerKey = vm.envUint("DEPLOYER_PRIVATE_KEY");
        vm.startBroadcast(deployerKey);
        deployed = new ReserveDecisionRegistry();
        vm.stopBroadcast();
        console2.log("ReserveDecisionRegistry deployed at:", address(deployed));
        console2.log("Chain ID:", block.chainid);
    }
}
