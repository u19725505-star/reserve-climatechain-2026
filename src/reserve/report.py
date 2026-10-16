"""
RESERVE — Processor Comparison Report

Purpose:
    Present the eligible processor ranking in a readable table.

The report displays screening estimates only. It does not claim
that any candidate is a verified low-emissions option.
"""


def format_processor_report(
    ranked_candidates: list[dict],
) -> str:
    """
    Format ranked processor results as a plain-text table.

    Args:
        ranked_candidates: Results returned by the ranking module.

    Returns:
        A string suitable for terminal output or saving to a file.
    """

    # Define the columns that will appear in the report.
    headers = [
        "Rank",
        "Processor",
        "Distance (km)",
        "Estimated emissions (kg CO2e)",
    ]

    # Prepare the rows, formatting numeric values consistently.
    rows = []

    for rank, candidate in enumerate(ranked_candidates, start=1):
        rows.append(
            [
                str(rank),
                str(candidate["processor"]),
                f'{candidate["distance_km"]:.1f}',
                f'{candidate["estimated_emissions_kg_co2e"]:.2f}',
            ]
        )

    # If no candidate qualifies, return a clear explanation.
    if not rows:
        return (
            "RESERVE Processor Comparison\n"
            "No eligible processors were found for this shipment."
        )

    # Calculate each column's width using both headings and values.
    column_widths = [
        max(len(headers[index]), *(len(row[index]) for row in rows))
        for index in range(len(headers))
    ]

    # Build a reusable function for formatting each table row.
    def format_row(values):
        return " | ".join(
            value.ljust(column_widths[index])
            for index, value in enumerate(values)
        )

    # Build the report from the title, headings, separator, and rows.
    separator = "-+-".join("-" * width for width in column_widths)

    lines = [
        "RESERVE Processor Comparison",
        "Ranked by estimated transport emissions (lowest first)",
        "",
        format_row(headers),
        separator,
    ]

    lines.extend(format_row(row) for row in rows)

    # Make the assumption visible so estimates are not mistaken
    # for measured or independently verified emissions.
    lines.extend(
        [
            "",
            "Note: emissions are screening estimates based on the",
            "supplied emission factor, not verified measurements.",
        ]
    )

    return "\n".join(lines)
