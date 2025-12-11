import os
from pathlib import Path
from tinkertool.scripts.create_ppe.config import SubmitPPEConfig
from tinkertool.scripts.create_ppe.create_ppe import submit_ppe

script_dir = Path(__file__).parent

# Subset of ensemble member IDs to continue
member_ids = {19, 21, 32, 65, 69}
wanted_names = {f"ensemble_member.{i:03d}" for i in member_ids}

# Collect existing directories
cases_dir = script_dir.parent
existing_dirs = [p for p in cases_dir.iterdir() if p.is_dir()]
found_names = {p.name for p in existing_dirs}

# Validate that all requested cases exist
missing = sorted(wanted_names - found_names)
if missing:
    raise FileNotFoundError(f"The following requested cases were not found: {', '.join(missing)}")

# Build the cases list and sort numerically by the ID
cases = [p for p in existing_dirs if p.name in wanted_names]
cases.sort(key=lambda p: int(p.name.split(".")[-1]))

# Optional: preflight check that case.submit exists and is executable
bad = []
for case in cases:
    submit_path = case / "case.submit"
    if not submit_path.is_file() or not os.access(submit_path, os.X_OK):
        bad.append(case.name)
if bad:
    raise FileNotFoundError(f"Missing or non-executable 'case.submit' in: {', '.join(bad)}")

# Prepare logging directory
log_dir = script_dir.joinpath('output_files', 'logs')
log_dir.mkdir(parents=True, exist_ok=True)

# Create config (append mode to avoid overwriting logs)
submit_config = SubmitPPEConfig(
    cases    = cases,
    verbose  = 2,
    log_dir  = log_dir,
    log_mode = 'a',  # append, not overwrite
)

# Submit the cases
submit_ppe(config=submit_config)

# print(f"CASES: {cases}")
# print()
# print(f"CONFIG: {submit_config}")