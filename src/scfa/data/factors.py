"""Factor definitions for the supply chain sustainability study."""

FACTOR_CODES = ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11"]

FACTOR_NAMES = {
    "F1":  "Customer Awareness",
    "F2":  "Global Image",
    "F3":  "Government Policies",
    "F4":  "Lack of Complete Information",
    "F5":  "Lack of Expertise",
    "F6":  "Media",
    "F7":  "Rail/Road/Sea Infrastructure",
    "F8":  "Governance Mechanism",
    "F9":  "Collaborations",
    "F10": "Working Conditions at Plant",
    "F11": "Sales and Marketing Activity",
}

N = len(FACTOR_CODES)

# Short labels used in plots
FACTOR_LABELS = [
    "F1-CustAware",
    "F2-GlobImage",
    "F3-GovtPolicy",
    "F4-LackInfo",
    "F5-LackExpert",
    "F6-Media",
    "F7-Infra",
    "F8-Governance",
    "F9-Collab",
    "F10-WorkCond",
    "F11-SalesMktg",
]
