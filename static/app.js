const form = document.querySelector("#shipment-form");
const results = document.querySelector("#processor-results");
const errorBox = document.querySelector("#form-error");
const statusBox = document.querySelector("#run-status");

function escapeHTML(value) {
  return String(value).replace(/[&<>"']/g, (char) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
  })[char]);
}

function formatNumber(value, digits = 1) {
  return Number(value).toLocaleString(undefined, {
    maximumFractionDigits: digits,
    minimumFractionDigits: 0
  });
}

function renderProcessor(processor, maxEmissions) {
  const eligible = processor.eligible;
  const rank = processor.rank ? `#${processor.rank}` : "—";
  const reasons = (processor.reasons || []).map(reason =>
    `<li>${escapeHTML(reason)}</li>`
  ).join("");
  const width = maxEmissions > 0
    ? Math.max(2, processor.estimated_emissions_kg_co2e / maxEmissions * 100)
    : 0;

  return `
    <article class="processor-card">
      <div class="processor-main">
        <div class="processor-name">
          <span class="rank-number">${rank}</span>
          <span>${escapeHTML(processor.name)}</span>
        </div>
        <span class="status ${eligible ? "" : "excluded"}">${eligible ? "ELIGIBLE" : "EXCLUDED"}</span>
      </div>
      <div class="processor-meta">
        <span>${formatNumber(processor.distance_km)} km</span>
        <span>${formatNumber(processor.capacity_tonnes)} t capacity</span>
        <span>Quality ${formatNumber(processor.quality_score, 2)}</span>
        <span>≈ ${formatNumber(processor.estimated_emissions_kg_co2e, 2)} kg CO₂e*</span>
      </div>
      ${reasons ? `<ul class="reason-list">${reasons}</ul>` : ""}
      <div class="emissions-track" title="Illustrative transport estimate relative to the highest estimate shown"><span style="width:${width}%"></span></div>
    </article>`;
}

async function evaluateScenario(event) {
  event.preventDefault();
  errorBox.textContent = "";
  statusBox.textContent = "EVALUATING…";

  const payload = {
    material: document.querySelector("#material").value,
    quantity_tonnes: Number(document.querySelector("#quantity").value),
    required_quality: Number(document.querySelector("#quality").value),
    earliest_delivery_day: Number(document.querySelector("#earliest").value),
    latest_delivery_day: Number(document.querySelector("#latest").value)
  };

  if (!Number.isFinite(payload.quantity_tonnes) || payload.quantity_tonnes <= 0 ||
      !Number.isFinite(payload.required_quality) || payload.required_quality < 0 ||
      payload.required_quality > 1 || payload.latest_delivery_day < payload.earliest_delivery_day) {
    statusBox.textContent = "CHECK INPUTS";
    errorBox.textContent = "Check the quantity, quality range, and delivery window.";
    return;
  }

  const button = form.querySelector('button[type="submit"]');
  button.disabled = true;
  button.querySelector("span").textContent = "Evaluating…";

  try {
    const response = await fetch("/api/evaluate", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "The evaluation could not be completed.");

    document.querySelector("#checked-count").textContent = data.processors.length;
    document.querySelector("#eligible-count").textContent = data.eligible_count;
    document.querySelector("#excluded-count").textContent = data.excluded_count;
    document.querySelector("#ranking-note").textContent =
      data.eligible_count ? "Estimated emissions vs eligible baseline" : "No eligible candidates";
    statusBox.textContent = "EVALUATION COMPLETE";

    const maxEmissions = Math.max(...data.processors.map(p => p.estimated_emissions_kg_co2e), 1);
    const ordered = [...data.processors].sort((a, b) => {
      if (a.eligible !== b.eligible) return a.eligible ? -1 : 1;
      if (a.eligible && a.rank !== b.rank) return a.rank - b.rank;
      return a.distance_km - b.distance_km;
    });
    results.innerHTML = ordered.map(p => renderProcessor(p, maxEmissions)).join("");

    const baseline = data.baseline;
    const selected = data.selected;
    const comparison = data.comparison || {};
    let baselineText = baseline.processor
      ? `Fair baseline (nearest eligible): ${baseline.processor}, ${formatNumber(baseline.estimated_emissions_kg_co2e, 2)} kg CO₂e. `
      : "No eligible baseline exists for this shipment. ";
    baselineText += selected
      ? `RESERVE selects ${selected} (${formatNumber(comparison.selected_estimated_emissions_kg_co2e, 2)} kg CO₂e). `
      : "RESERVE found no eligible processor. ";
    if (comparison.estimated_reduction_percent !== null &&
        comparison.estimated_reduction_percent !== undefined) {
      const delta = Number(comparison.estimated_reduction_percent);
      const label = delta > 0 ? "lower" : delta < 0 ? "higher" : "the same";
      baselineText += `Modeled estimate is ${label} by ${formatNumber(Math.abs(delta), 2)}% versus the eligible baseline. `;
    }
    baselineText += "Scenario only; not measured or verified savings.";
    document.querySelector("#baseline-text").textContent = baselineText;

    // This is a local browser-session audit trail, not a blockchain or server ledger.
    appendAuditEvent({
      action: "processor_evaluation",
      material: data.shipment.material,
      quantity_tonnes: data.shipment.quantity_tonnes,
      eligible_count: data.eligible_count,
      excluded_count: data.excluded_count,
      selected: data.selected,
      created_at: new Date().toISOString()
    });
  } catch (error) {
    statusBox.textContent = "EVALUATION FAILED";
    errorBox.textContent = error.message || "Could not contact the demo service.";
  } finally {
    button.disabled = false;
    button.querySelector("span").textContent = "Evaluate processors";
  }
}

let previousHash = "GENESIS";

async function appendAuditEvent(event) {
  const container = document.querySelector("#audit-events");
  if (!container) return;

  const serialized = JSON.stringify({previous_hash: previousHash, event});
  let digest = "SHA-256 unavailable";
  if (globalThis.crypto && crypto.subtle) {
    const bytes = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(serialized));
    digest = [...new Uint8Array(bytes)].map(b => b.toString(16).padStart(2, "0")).join("");
    previousHash = digest;
  }

  const row = document.createElement("article");
  row.className = "audit-event";
  const time = new Date(event.created_at).toLocaleTimeString();
  row.innerHTML = `<span class="audit-dot"></span><div><b>Processor evaluation</b><p>${escapeHTML(event.material)} · ${escapeHTML(event.quantity_tonnes)} tonnes · ${escapeHTML(event.eligible_count)} eligible · ${escapeHTML(event.excluded_count)} excluded</p><small>${escapeHTML(time)} · ${escapeHTML(digest.slice(0, 18))}…</small></div>`;
  container.prepend(row);
}

form.addEventListener("submit", evaluateScenario);
form.addEventListener("reset", () => {
  setTimeout(() => {
    errorBox.textContent = "";
    statusBox.textContent = "READY TO RUN";
    document.querySelector("#checked-count").textContent = "—";
    document.querySelector("#eligible-count").textContent = "—";
    document.querySelector("#excluded-count").textContent = "—";
    document.querySelector("#ranking-note").textContent = "Run a scenario to rank";
    results.innerHTML = '<div class="empty-state"><span>↘</span><b>Your results appear here.</b><p>Run the example to see eligibility decisions, exclusion reasons and the ranked candidates.</p></div>';
    document.querySelector("#baseline-text").textContent = "Compare the nearest processor with the eligibility-screened result.";
  }, 0);
});


async function runExplainableDecisionSupport() {
  const button = document.querySelector("#run-ai");
  const output = document.querySelector("#ai-results");
  if (!button || !output) return;
  button.disabled = true;
  button.textContent = "Scoring eligible candidates…";
  const payload = {
    material: document.querySelector("#material").value,
    quantity_tonnes: Number(document.querySelector("#quantity").value),
    required_quality: Number(document.querySelector("#quality").value),
    earliest_delivery_day: Number(document.querySelector("#earliest").value),
    latest_delivery_day: Number(document.querySelector("#latest").value)
  };
  try {
    const response = await fetch("/api/decision-support", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload)
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error || "Decision support failed.");
    const cards = data.candidates.map(candidate => {
      const criteria = Object.entries(candidate.criteria).map(([key, value]) =>
        "<span>" + escapeHTML(key.replaceAll("_", " ")) + ": " + formatNumber(value * 100, 1) + "%</span>"
      ).join("");
      return "<article class=\"processor-card\">" +
        "<div class=\"processor-main\"><div class=\"processor-name\"><span class=\"rank-number\">#" + candidate.ai_rank +
        "</span><span>" + escapeHTML(candidate.processor) + "</span></div><strong>" + formatNumber(candidate.score_percent, 1) + " / 100</strong></div>" +
        "<p>" + escapeHTML(candidate.explanation) + "</p><div class=\"criteria-grid\" style=\"display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin:14px 0 10px\">" + criteria.replaceAll("<span>", "<span style=\"display:block;min-width:0;padding:8px 10px;border-radius:5px;background:#f1f3eb;line-height:1.5;overflow-wrap:anywhere\">") + "</div>" +
        "<small>Illustrative score; not a trained or operationally validated model.</small></article>";
    }).join("");
    const limitations = data.limitations.map(x => "<li>" + escapeHTML(x) + "</li>").join("");
    output.innerHTML = "<div class=\"baseline-box\"><div class=\"baseline-symbol\">✳</div><div><span class=\"mini-label\">" +
      escapeHTML(data.model) + " · " + escapeHTML(data.status) + "</span><p>Weights: transport 45% · quality 20% · capacity 20% · delivery fit 15%. Hard eligibility rules remain mandatory.</p></div></div>" +
      (cards || "<p>No eligible candidates for this shipment.</p>") +
      "<div class=\"integrity-banner\"><span class=\"integrity-mark\">i</span><div><b>Model limitations</b><ul>" + limitations +
      "</ul><p>Audit event #" + data.audit.event_sequence + " · SHA-256 " + escapeHTML(data.audit.event_hash) + " · " +
      escapeHTML(data.audit.ledger_type) + "</p></div></div>";
    const status = document.querySelector("#ledger-status");
    if (status) status.textContent = "EVENT RECORDED · #" + data.audit.event_sequence;
  } catch (error) {
    output.textContent = error.message || "Could not run decision support.";
  } finally {
    button.disabled = false;
    button.textContent = "Run decision support →";
  }
}

async function verifyServerAuditChain() {
  const button = document.querySelector("#verify-ledger");
  const status = document.querySelector("#ledger-status");
  const output = document.querySelector("#ai-results");
  if (!button || !status) return;
  button.disabled = true;
  button.textContent = "Verifying…";
  try {
    const response = await fetch("/api/audit/verify", {method: "POST"});
    const data = await response.json();
    if (!response.ok) throw new Error("Audit verification failed.");
    status.textContent = data.valid ? "CHAIN VALID · " + data.event_count + " EVENTS" : "CHAIN INVALID";
    status.className = "evidence-status " + (data.valid ? "" : "pending-text");
    if (output) {
      const note = data.limitation || "No audit events have been recorded yet.";
      output.insertAdjacentHTML("afterbegin", "<div class=\"baseline-box\"><div class=\"baseline-symbol\">✓</div><div><span class=\"mini-label\">AUDIT VERIFICATION</span><p>" +
        escapeHTML(data.ledger_type || "Local hash chain") + ": " + (data.valid ? "valid" : "invalid") + " · " + data.event_count +
        " event(s). " + escapeHTML(note) + "</p>" + (data.head_hash ? "<small>Chain head: " + escapeHTML(data.head_hash) + "</small>" : "") + "</div></div>");
    }
  } catch (error) {
    status.textContent = "VERIFICATION FAILED";
    if (output) output.textContent = error.message || "Could not verify audit chain.";
  } finally {
    button.disabled = false;
    button.textContent = "Verify audit chain →";
  }
}

document.querySelector("#run-ai")?.addEventListener("click", runExplainableDecisionSupport);
document.querySelector("#verify-ledger")?.addEventListener("click", verifyServerAuditChain);


async function anchorAuditDigest() {
  const button = document.querySelector("#anchor-on-chain");
  const status = document.querySelector("#chain-transaction-status");
  if (!button || !status) return;
  const address = (button.dataset.contractAddress || "").trim();
  const chainId = Number(button.dataset.chainId || "11155111");
  if (!address) { status.textContent = "Set RESERVE_CONTRACT_ADDRESS after contract deployment."; return; }
  if (!window.ethereum || !window.ethers) { status.textContent = "A browser wallet and ethers library are required."; return; }
  button.disabled = true;
  try {
    const provider = new ethers.BrowserProvider(window.ethereum);
    await provider.send("eth_requestAccounts", []);
    let network = await provider.getNetwork();
    if (Number(network.chainId) !== chainId) {
      if (chainId !== 11155111) throw new Error("Switch your wallet to chain ID " + chainId + ".");
      try {
        await window.ethereum.request({method:"wallet_switchEthereumChain",params:[{chainId:"0xaa36a7"}]});
      } catch (switchError) {
        if (switchError.code !== 4902) throw switchError;
        await window.ethereum.request({method:"wallet_addEthereumChain",params:[{
          chainId:"0xaa36a7",
          chainName:"Ethereum Sepolia",
          nativeCurrency:{name:"Sepolia Ether",symbol:"ETH",decimals:18},
          rpcUrls:["https://ethereum-sepolia-rpc.publicnode.com"],
          blockExplorerUrls:["https://sepolia.etherscan.io"]
        }]});
      }
      network = await provider.getNetwork();
    }
    if (Number(network.chainId) !== chainId) throw new Error("Wallet is on the wrong network.");
    if (!ethers.isAddress(address)) throw new Error("Configured contract address is invalid.");
    const auditResponse = await fetch("/api/audit");
    const audit = await auditResponse.json();
    if (!auditResponse.ok || !audit.valid || !audit.event_count || !audit.head_hash) {
      throw new Error("Run decision support first and verify a non-empty audit chain.");
    }
    const abi = [
      "function recordCount() view returns (uint64)",
      "function latestRecordHash() view returns (bytes32)",
      "function anchorDecision(bytes32,bytes32,bytes32) returns (uint64)"
    ];
    const contract = new ethers.Contract(address, abi, await provider.getSigner());
    const previous = await contract.latestRecordHash();
    const modelHash = ethers.keccak256(ethers.toUtf8Bytes("RESERVE-XAI-MCDM-0.1"));
    const digest = ethers.keccak256(ethers.AbiCoder.defaultAbiCoder().encode(
      ["string","uint256","bytes32","bytes32"],
      ["RESERVE-AUDIT-ANCHOR-v1",BigInt(audit.event_count),"0x" + audit.head_hash.replace(/^0x/, ""),modelHash]
    ));
    status.textContent = "Review and approve the transaction in your wallet.";
    const tx = await contract.anchorDecision(digest, previous, modelHash);
    status.textContent = "Submitted: " + tx.hash + " — waiting for confirmation.";
    const receipt = await tx.wait();
    if (!receipt || receipt.status !== 1) throw new Error("Transaction confirmation failed.");
    status.textContent = "Confirmed in block " + receipt.blockNumber + ". Transaction: " + tx.hash + " ";
    const link = document.createElement("a");
    link.href = "https://sepolia.etherscan.io/tx/" + encodeURIComponent(tx.hash);
    link.target = "_blank";
    link.rel = "noopener noreferrer";
    link.textContent = "View on Sepolia explorer";
    status.appendChild(link);
  } catch (error) {
    status.textContent = error && error.message ? error.message : "Anchoring failed.";
  } finally {
    button.disabled = false;
  }
}
document.querySelector("#anchor-on-chain")?.addEventListener("click", anchorAuditDigest);


// Local blockchain demonstration. This intentionally does not create a real
// wallet, private key, signed transaction, or public-chain transaction.
const demoChain = [];
let demoIdentity = null;

function demoHex(bytes) {
  return [...bytes].map(byte => byte.toString(16).padStart(2, "0")).join("");
}

async function sha256Hex(value) {
  if (!globalThis.crypto || !crypto.subtle) {
    throw new Error("Secure browser hashing is unavailable. Open RESERVE over HTTPS.");
  }
  const bytes = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return demoHex(new Uint8Array(bytes));
}

function setDemoStatus(message, warning = false) {
  const status = document.querySelector("#demo-chain-status");
  if (!status) return;
  status.textContent = message;
  status.className = "evidence-status" + (warning ? " pending-text" : "");
}

async function createDemoIdentity() {
  const button = document.querySelector("#create-demo-wallet");
  if (!button) return;
  button.disabled = true;
  try {
    const random = new Uint8Array(16);
    crypto.getRandomValues(random);
    demoIdentity = "RESERVE-DEMO-" + demoHex(random).toUpperCase();
    document.querySelector("#demo-wallet-address").textContent =
      demoIdentity + " — temporary demo label only; no private key or funds exist.";
    document.querySelector("#anchor-demo-record").disabled = false;
    document.querySelector("#verify-demo-chain").disabled = false;
    setDemoStatus("TEMPORARY DEMO IDENTITY READY");
  } catch (error) {
    setDemoStatus(error.message || "Could not create demo identity.", true);
  } finally {
    button.disabled = false;
  }
}

async function anchorDemoRecord() {
  const button = document.querySelector("#anchor-demo-record");
  if (!button || !demoIdentity) return;
  button.disabled = true;
  try {
    const response = await fetch("/api/audit");
    const audit = await response.json();
    if (!response.ok || !audit.valid) throw new Error("The server audit chain did not verify.");
    if (!audit.event_count || !audit.head_hash) {
      throw new Error("Run decision support above first so there is an audit event to anchor.");
    }
    const previousHash = demoChain.length ? demoChain[demoChain.length - 1].recordHash : "GENESIS";
    const payload = {
      sequence: demoChain.length + 1,
      identity: demoIdentity,
      auditEventCount: audit.event_count,
      auditHeadHash: audit.head_hash,
      previousHash,
      modelVersion: "RESERVE-XAI-MCDM-0.1",
      network: "LOCAL-DEMO-SIMULATION"
    };
    const recordHash = await sha256Hex(JSON.stringify(payload));
    demoChain.push({...payload, recordHash});
    document.querySelector("#demo-record-summary").textContent =
      "Record #" + payload.sequence + " · audit events " + payload.auditEventCount +
      " · SHA-256 " + recordHash + " · previous " + previousHash.slice(0, 18) + "…";
    document.querySelector("#demo-verification-result").textContent =
      "Record added to the in-memory demo chain. This is not a public-chain transaction.";
    setDemoStatus("DEMO RECORD " + payload.sequence + " CREATED");
  } catch (error) {
    document.querySelector("#demo-record-summary").textContent =
      error.message || "Could not create demo record.";
    setDemoStatus("RECORD NOT CREATED", true);
  } finally {
    button.disabled = false;
  }
}

async function verifyDemoChain() {
  const button = document.querySelector("#verify-demo-chain");
  if (!button) return;
  button.disabled = true;
  try {
    let previousHash = "GENESIS";
    for (let i = 0; i < demoChain.length; i += 1) {
      const record = demoChain[i];
      const {recordHash, ...payload} = record;
      if (payload.sequence !== i + 1 || payload.previousHash !== previousHash) {
        throw new Error("Sequence or previous-record link mismatch at record #" + (i + 1) + ".");
      }
      const computed = await sha256Hex(JSON.stringify(payload));
      if (computed !== recordHash) throw new Error("Hash mismatch at record #" + (i + 1) + ".");
      previousHash = recordHash;
    }
    document.querySelector("#demo-verification-result").textContent =
      "PASS — " + demoChain.length + " record(s) verified; each digest and previous-record link matches. " +
      "Verification covers this browser session only, not a decentralized network.";
    setDemoStatus("DEMO CHAIN VALID · " + demoChain.length + " RECORDS");
  } catch (error) {
    document.querySelector("#demo-verification-result").textContent = error.message || "Verification failed.";
    setDemoStatus("DEMO CHAIN INVALID", true);
  } finally {
    button.disabled = false;
  }
}

document.querySelector("#create-demo-wallet")?.addEventListener("click", createDemoIdentity);
document.querySelector("#anchor-demo-record")?.addEventListener("click", anchorDemoRecord);
document.querySelector("#verify-demo-chain")?.addEventListener("click", verifyDemoChain);
