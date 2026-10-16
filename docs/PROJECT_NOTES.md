# RESERVE — Project Notes

## 1. Project purpose

RESERVE is a prototype for evaluating and ranking candidate material processors before a shipment is dispatched. The goal is to help make processor selection more transparent by considering eligibility, processing capacity, quality requirements, delivery windows, distance, and estimated transport emissions.

## 2. Current implementation

The Python prototype is organized into the following modules:

* `src/reserve/evaluation.py` — checks whether a processor meets the shipment's basic requirements.
* `src/reserve/emissions.py` — estimates transport emissions from distance, shipment quantity, and a supplied emission factor.
* `src/reserve/ranking.py` — ranks eligible processors by estimated transport emissions.
* `src/reserve/report.py` — formats processor comparisons into a readable report.
* `src/reserve/demo.py` — runs a small end-to-end example using synthetic shipment and processor data.

Automated tests cover evaluation, emissions calculations, ranking, report formatting, and workflow behavior.

## 3. Current demonstration

The example uses synthetic data for a recycled-plastic shipment of 10 tonnes. It checks four candidate processors, excludes candidates that fail the eligibility checks, and ranks the remaining candidates.

The demonstration uses an illustrative emission factor of 0.1 kg CO2e per tonne-kilometre. This factor has not been independently verified for the intended transport scenario.

## 4. Current limitations

* The demonstration uses synthetic data, not a real operational shipment or processor network.
* The emission factor is illustrative rather than a validated, source-backed factor.
* Estimated transport emissions are screening estimates, not measured emissions.
* The current ranking does not establish that RESERVE reduces emissions compared with an existing dispatch process.
* No real-world pilot or independently validated climate benefit has been demonstrated.
* The local code should not be described as a decentralized blockchain. Any future audit history must be described accurately according to its actual implementation.

## 5. Next development step

Add a structured JSON output for each processor comparison. The output should record the shipment inputs, candidate processor results, eligibility decisions, estimated emissions, the emission factor used, and clear warnings that the example data and factor are illustrative.

Add automated tests to verify that the JSON output is valid, contains the expected fields, and preserves the distinction between estimates and verified measurements.

## 6. Validation priorities

1. Keep the existing automated tests passing.
2. Test the JSON output with both eligible and ineligible processors.
3. Record the assumptions behind every emissions estimate.
4. Find credible, applicable transport-emissions factors and document their sources before making climate-impact claims.
5. Compare RESERVE against a clearly defined baseline using the same shipment and processor constraints.
6. Report unfavorable or inconclusive results honestly.

## 7. Evidence standard

Distinguish implemented functionality, synthetic demonstrations, experimental results, and real-world evidence. Do not claim measured emissions reductions, operational deployment, or proven climate impact without supporting evidence.
