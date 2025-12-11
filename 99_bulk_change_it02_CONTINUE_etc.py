from pathlib import Path
from tinkertool.scripts.create_ppe.create_ppe import bulk_xmlchange

script_dir = Path(__file__).parent

# Specify the subset of ensemble member IDs
member_ids = {19, 21, 32, 65, 69}
wanted_names = {f"ensemble_member.{i:03d}" for i in member_ids}

# Collect existing directories once
cases_dir = script_dir.parent
existing_dirs = [p for p in cases_dir.iterdir() if p.is_dir()]
found_names = {p.name for p in existing_dirs}

# Validate that all requested cases exist; fail if any are missing
missing = sorted(wanted_names - found_names)
if missing:
    raise FileNotFoundError(f"The following requested cases were not found: {', '.join(missing)}")

# Build the cases list and sort numerically by the ID
cases = [p for p in existing_dirs if p.name in wanted_names]
cases.sort(key=lambda p: int(p.name.split(".")[-1]))

# Changes to apply
change = {
    'CONTINUE_RUN': 'TRUE',
    'STOP_N': '25',
    'STOP_OPTION': 'nyears',
    'JOB_WALLCLOCK_TIME': {
        'case.run': '45:00:00',
        'case.st_archive': '10:00:00',
        'case.compress': '18:00:00'
    }
}

# Apply changes
bulk_xmlchange(cases, change)

# print(f"CASES: {cases}")

# print(f"CHANGE: {change}")