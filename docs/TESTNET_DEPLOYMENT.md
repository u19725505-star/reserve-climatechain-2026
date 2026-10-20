# Testnet Deployment Notes

## Current status
The repository contains a Solidity registry prototype and Foundry tests. A public/testnet deployment and live on-chain transaction integration have **not** been verified. The local SHA-256 audit log is a separate component and must not be described as decentralized blockchain storage.

## Before deployment
- Review the contract and its access-control assumptions.
- Confirm the exact compiler version, dependency versions, and build configuration.
- Run the full Foundry test suite and add tests for expected and adversarial cases.
- Decide what data is appropriate to publish; store hashes or references rather than confidential shipment or personal data.
- Document chain ID, RPC provider, deployment account, and key-management plan.
- Use a dedicated test account and protect private keys outside the repository and logs.
- Define how the deployed contract address and bytecode will be independently verified.

## Example validation sequence
From the repository root, with Foundry installed and dependencies configured:

```bash
forge test -vvv
forge build
```

A successful local test or build is not evidence that the contract has been deployed. Deployment commands depend on the selected network and project configuration and should only be run after the pre-deployment review.

## Evidence to publish after a real testnet deployment
- network name and chain ID;
- contract address and verified explorer link;
- deployment transaction hash;
- compiler and source verification details;
- test results and known limitations;
- an explicit statement describing whether the application actually submits transactions.

Do not publish private keys, seed phrases, RPC secrets, or sensitive shipment data.

## Relationship to the app
Until an integration is implemented and demonstrated, describe the Solidity registry as a separate prototype. Do not imply the live Flask application writes to it.
