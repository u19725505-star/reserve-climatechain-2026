# Testnet deployment and browser-wallet integration

## Current integration state

The web app now contains a browser-wallet anchoring interface. It is disabled unless `RESERVE_CONTRACT_ADDRESS` is configured. Once configured, it asks the user to connect a browser wallet on the configured chain and submits an explicit transaction to `ReserveDecisionRegistry.anchorDecision`. The app never receives the wallet's private key.

The page anchors a digest computed from the local audit-chain head, event count, and model-version hash. The contract stores the digest, previous on-chain digest, model-version digest, block timestamp, and submitting address. It does **not** upload the raw audit log or prove that underlying data are true.

## What is required to activate it

1. Use a dedicated testnet wallet with only test funds. Never use a production wallet or commit credentials.
2. Obtain a Sepolia RPC endpoint and test ETH from reputable sources.
3. From a trusted local development environment, install Foundry and run `forge test -vvv`.
4. Set `SEPOLIA_RPC_URL` and `DEPLOYER_PRIVATE_KEY` as local shell environment variables; do not put them in source control, notebooks, logs, or screenshots.
5. Deploy using the script below. Review the network, account, and estimated transaction costs before broadcasting.

```bash
forge test -vvv
forge script script/DeployReserveDecisionRegistry.s.sol:DeployReserveDecisionRegistry \
  --rpc-url "$SEPOLIA_RPC_URL" --broadcast -vvvv
```

6. Confirm the deployment transaction and contract address on Sepolia Etherscan. Verify the deployed bytecode/source and confirm chain ID 11155111. Record the deployment transaction, address, deployer, compiler settings, and source commit.
7. Configure the Render web service with:
   - `RESERVE_CONTRACT_ADDRESS=<verified deployed address>`
   - `RESERVE_CHAIN_ID=11155111`
8. Redeploy/restart the web service, open the site in a browser with an injected wallet, run decision support to create an audit event, verify the local audit chain, then select **Connect wallet & anchor audit hash**. Approve the transaction in the wallet and verify the resulting transaction independently on Sepolia Etherscan.

## Important constraints

- The repository workflow does not deploy automatically; the deploy script is explicit and manual.
- The browser-wallet UI remains disabled until a deployed contract address is configured.
- Testnet transactions cost test ETH and may be publicly visible. Only a digest and non-sensitive model version are submitted.
- The local hash-chain file may be ephemeral on the current hosting plan. The UI must not claim durable history unless persistence is configured and tested.
- A transaction proves that a wallet submitted a digest to a contract. It does not prove the factual accuracy of processor profiles, shipment quantities, emissions factors, or climate outcomes.
- This is a testnet proof-of-integration, not production readiness. Before production use, conduct an independent contract/security review, threat model, access-control review, privacy assessment, backup/retention design, and an operational pilot with source-backed emissions data.
