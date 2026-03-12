from pathlib import Path
from datetime import datetime
from tinkertool.scripts.create_ppe.config import SubmitPPEConfig
from tinkertool.scripts.create_ppe.create_ppe import submit_ppe
script_dir = Path(__file__).parent

cases_dir = (script_dir / ".." / ".." / "cases-mini_ppe").resolve()

# Specify the subset to submit
selected_members = [
    "016", "021", "027", "028", "033", "036",
    "040", "041", "042", "043", "044", "045",
    "046", "047", "048", "049", "050",
    "051", "052", "053", "054", "055",
    "056", "057", "058", "059", "060",
]

# Normalise to directory names "ensemble_member.xxx"
selected = set()
for a in selected_members:
    a = str(a).strip()
    if not a:
        continue
    if a.startswith("ensemble_member."):
        selected.add(a)
    else:
        try:
            selected.add(f"ensemble_member.{int(a):03d}")
        except ValueError:
            raise SystemExit(f"Invalid member spec: {a!r}")

# Require at least one valid member
if not selected:
    raise SystemExit("No valid members specified in selected_members.")

# Collect only requested cases and fail if any are missing
cases = []
missing = []
for name in sorted(selected):
    p = cases_dir / name
    if p.is_dir():
        cases.append(p)
    else:
        missing.append(name)

if missing:
    raise SystemExit(
        f"Missing case directories under {cases_dir}:\n  " + "\n  ".join(missing)
    )

# If none collected, fail
if not cases:
    raise SystemExit("No cases collected; aborting.")

# Sort cases by name (numeric order preserved by zero-padding)
cases.sort(key=lambda x: x.name)

# print(cases)

current_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

submit_config = SubmitPPEConfig(
    cases       = cases,
    verbose     = 2,
    log_dir     = script_dir.joinpath('output_files', 'logs'),
    log_mode    = 'w'
)

submit_ppe(config=submit_config)