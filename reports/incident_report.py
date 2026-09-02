from datetime import datetime
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_incident_report(
    drift_event,
    remediation_result=None,
    output_path=None,
):
    """
    Generate a PDF incident report for an AeroDrift security event.
    """

    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = f"reports/incident_{timestamp}.pdf"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    document = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph(
            "AeroDrift Incident Report",
            styles["Title"],
        )
    )

    elements.append(Spacer(1, 15))

    generated_at = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    elements.append(
        Paragraph(
            f"<b>Report Generated:</b> {generated_at}",
            styles["Normal"],
        )
    )

    elements.append(Spacer(1, 20))

    incident_data = [
        ["Field", "Value"],
        [
            "Event Type",
            str(drift_event.get("event_type", "N/A")),
        ],
        [
            "Resource Type",
            str(drift_event.get("resource_type", "N/A")),
        ],
        [
            "Resource ID",
            str(drift_event.get("resource_id", "N/A")),
        ],
        [
            "Severity",
            str(drift_event.get("severity", "N/A")),
        ],
        [
            "CIDR",
            str(drift_event.get("cidr", "N/A")),
        ],
        [
            "Protocol",
            str(drift_event.get("protocol", "N/A")),
        ],
        [
            "From Port",
            str(drift_event.get("from_port", "N/A")),
        ],
        [
            "To Port",
            str(drift_event.get("to_port", "N/A")),
        ],
    ]

    incident_table = Table(
        incident_data,
        colWidths=[150, 330],
    )

    incident_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    colors.HexColor("#1F4E78"),
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    colors.white,
                ),
                (
                    "FONTNAME",
                    (0, 0),
                    (-1, 0),
                    "Helvetica-Bold",
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    colors.grey,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (0, -1),
                    colors.HexColor("#EAF2F8"),
                ),
            ]
        )
    )

    elements.append(
        Paragraph(
            "Detected Incident",
            styles["Heading2"],
        )
    )

    elements.append(Spacer(1, 8))
    elements.append(incident_table)
    elements.append(Spacer(1, 20))

    if remediation_result:
        remediation_data = [
            ["Field", "Value"],
            [
                "Status",
                str(
                    remediation_result.get(
                        "status",
                        "N/A",
                    )
                ),
            ],
            [
                "Resource ID",
                str(
                    remediation_result.get(
                        "resource_id",
                        "N/A",
                    )
                ),
            ],
            [
                "Event Type",
                str(
                    remediation_result.get(
                        "event_type",
                        "N/A",
                    )
                ),
            ],
            [
                "Action",
                (
                    "Revoke unauthorized public "
                    "security group ingress"
                ),
            ],
        ]

        remediation_table = Table(
            remediation_data,
            colWidths=[150, 330],
        )

        remediation_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.HexColor("#2E7D32"),
                    ),
                    (
                        "TEXTCOLOR",
                        (0, 0),
                        (-1, 0),
                        colors.white,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "BACKGROUND",
                        (0, 1),
                        (0, -1),
                        colors.HexColor("#E8F5E9"),
                    ),
                ]
            )
        )

        elements.append(
            Paragraph(
                "Remediation Details",
                styles["Heading2"],
            )
        )

        elements.append(Spacer(1, 8))
        elements.append(remediation_table)
        elements.append(Spacer(1, 20))

    elements.append(
        Paragraph(
            "Incident Summary",
            styles["Heading2"],
        )
    )

    summary_text = (
        "AeroDrift detected an unauthorized public ingress "
        "configuration affecting a cloud security group. "
        "The event was classified as a security drift and "
        "processed by the remediation engine."
    )

    elements.append(
        Paragraph(
            summary_text,
            styles["BodyText"],
        )
    )

    document.build(elements)

    return output_path
