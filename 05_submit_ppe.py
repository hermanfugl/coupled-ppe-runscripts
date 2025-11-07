import sys
from pathlib import Path
from datetime import datetime
from tinkertool.scripts.create_ppe.config import SubmitPPEConfig
from tinkertool.scripts.create_ppe.create_ppe import submit_ppe
script_dir = Path(__file__).parent

#collect all paths
cases = []
cases_dir = script_dir.parent
for case in cases_dir.iterdir():
    if case.is_dir():
        if 'ensemble_member' in case.name:
            cases.append(case)

# sort cases by name
cases.sort(key=lambda x: x.name)

# get current timestamp for log file
current_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

submit_config = SubmitPPEConfig(
    cases       = cases,
    verbose     = 2,
    log_dir     = script_dir.joinpath('output_files', 'logs'),
    log_mode    = 'w'
)

submit_ppe(config=submit_config)