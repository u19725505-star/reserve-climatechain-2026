// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "../contracts/ReserveDecisionRegistry.sol";

interface Vm {
    function prank(address sender) external;
}

contract ReserveDecisionRegistryTest {
    Vm private constant vm = Vm(address(uint160(uint256(keccak256("hevm cheat code")))));
    ReserveDecisionRegistry private registry;

    function setUp() public {
        registry = new ReserveDecisionRegistry();
    }

    function testAnchorGenesisAndLinkedSecondRecord() public {
        bytes32 first = keccak256("decision-one");
        bytes32 model = keccak256("model-v0.1");
        uint64 firstSequence = registry.anchorDecision(first, bytes32(0), model);
        require(firstSequence == 1, "first sequence");
        require(registry.latestRecordHash() == first, "first head");

        bytes32 second = keccak256("decision-two");
        uint64 secondSequence = registry.anchorDecision(second, first, model);
        require(secondSequence == 2, "second sequence");
        ReserveDecisionRegistry.DecisionRecord memory record = registry.getRecord(2);
        require(record.recordHash == second, "second hash");
        require(record.previousHash == first, "previous link");
        require(record.submitter == address(this), "submitter");
    }

    function testRejectWrongPreviousHash() public {
        bool reverted = false;
        try registry.anchorDecision(
            keccak256("decision"), keccak256("not-genesis"), keccak256("model")
        ) returns (uint64) {
            reverted = false;
        } catch {
            reverted = true;
        }
        require(reverted, "must reject broken chain link");
        require(registry.recordCount() == 0, "count must remain zero");
    }

    function testRejectUnauthorizedWriter() public {
        address stranger = address(0xBEEF);
        vm.prank(stranger);
        bool reverted = false;
        try registry.anchorDecision(
            keccak256("decision"), bytes32(0), keccak256("model")
        ) returns (uint64) {
            reverted = false;
        } catch {
            reverted = true;
        }
        require(reverted, "must reject unauthorized writer");
    }

    function testOwnerCanAuthorizeWriter() public {
        address writer = address(0xCAFE);
        registry.setWriter(writer, true);
        require(registry.authorizedWriters(writer), "writer authorized");
        vm.prank(writer);
        uint64 sequence = registry.anchorDecision(
            keccak256("decision"), bytes32(0), keccak256("model")
        );
        require(sequence == 1, "authorized writer can anchor");
    }
}
