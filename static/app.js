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
      data.eligible_count ? "Ranked by estimated transport emissions" : "No eligible candidates";
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
    let baselineText = `Nearest processor: ${baseline.processor}. `;
    baselineText += baseline.eligible
      ? "It passes the current eligibility checks."
      : `It would fail eligibility screening: ${(baseline.reasons || []).join(" ")}`;
    baselineText += selected
      ? ` RESERVE's top eligible candidate is ${selected}.`
      : " RESERVE found no eligible processor in this demonstration.";
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
