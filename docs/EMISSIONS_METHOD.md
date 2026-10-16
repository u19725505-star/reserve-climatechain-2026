# RESERVE emissions method and evidence policy

## What the current demo calculates

For a shipment with quantity in metric tonnes, a candidate route distance in kilometres, and a factor in kg CO2e per tonne-kilometre:

`estimated_transport_kg_co2e = distance_km × shipment_tonnes × factor_kg_co2e_per_tonne_km`

This is a screening estimate for transport only. It is not a full product or facility footprint and does not include processing energy, avoided disposal, recycled-content benefits, empty running, return legs, load factor, or other effects unless these are separately represented in the activity data and method.

## Evidence source to use for real deployment

The U.S. EPA SmartWay Shipper Tool estimates freight-related emissions and supports comparison of freight carrier performance. Its technical documentation describes carrier performance data by freight category and includes activity and emission estimation methods:

- EPA, *2024 SmartWay Online Shipper Tool: Technical Documentation* (data year 2023), EPA-420-B-24-048, November 2024: https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P101CTRC.TXT
- EPA SmartWay Sustainability Accounting and Reporting: https://www.epa.gov/smartway/smartway-sustainability-accounting-and-reporting
- EPA SmartWay High Performer Lists: https://www.epa.gov/smartway/smartway-high-performer-lists

These sources establish a defensible route to carrier-specific or mode-specific freight factors; they do **not** establish a factor for any fictional RESERVE processor. Carrier performance data may be category-specific and some reported values are performance-bin midpoints, not precise measurements for a particular shipment. A deployment should use the most appropriate current factor available for the actual carrier/category and document its data year.

## Provenance and unit requirements

A candidate-specific factor must have a source label. For production use, record at least the source URL, publication/data year, carrier or freight category, pollutant scope (CO2 versus CO2e), original units, conversion, and whether the value is measured, reported, averaged, or illustrative. Do not copy a number from a table without preserving the category and unit definitions. Do not mix grams per short-ton-mile with kg per metric-tonne-kilometre without an explicit conversion.

The code currently accepts candidate-specific factors in kg CO2e/(metric tonne-km) only when a source label is present. If no candidate-specific factor is supplied, it uses the legacy fallback factor of 0.1 for demonstration continuity. That fallback is **illustrative and unsourced**, must not be presented as an EPA value, and causes the ranking to be distance-equivalent when used for every candidate.

## Fair comparison

1. Apply identical material, capacity, quality, and delivery-window constraints to all candidates.
2. Use the nearest eligible candidate as the default distance-based baseline—not the nearest processor overall if it is infeasible.
3. Compare the recommended candidate and baseline with the same shipment quantity and compatible factor provenance.
4. Calculate modeled difference as `baseline_estimate - selected_estimate`; percent difference is that value divided by the baseline estimate, multiplied by 100 when the baseline is non-zero.
5. Positive modeled difference means the estimate is lower than the baseline; negative means it is higher; zero means no estimated improvement.
6. Label all such comparisons as modeled estimates, not measured or verified savings.

If both selected and baseline use the same fallback factor, the nearest-eligible baseline should produce 0% modeled improvement by construction. That is an honest result, not a failure of the audit.

## Current limitations

- Processor profiles and shipment scenarios are fictional.
- The fallback factor of 0.1 is illustrative, not source-validated.
- No real carrier-specific factors or operational shipment records are currently attached to the fictional processors.
- No measured baseline, pilot, or verified emissions reduction has been established.
- The app's demonstration is therefore a prototype of eligibility-constrained decision support, not evidence of real-world climate impact.
