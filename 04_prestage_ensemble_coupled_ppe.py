import sys
from pathlib import Path
from tinkertool.scripts.create_ppe.config import PrestageEnsembleConfig
from tinkertool.scripts.create_ppe.create_ppe import prestage_ensemble
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

prestage_ensemble_config = PrestageEnsembleConfig(
    cases       = cases,
    verbose     = 2,
    log_dir     = Path(f'/cluster/projects/nn9560k/johannef/NorESM_workdir/cases-test_tinkertool4coupled/run_scripts/output_files/logs').resolve(),
    log_mode    = 'w'
)

if prestage_ensemble(prestage_ensemble_config):
    print("All cases are built correctly.")
else:
    print("Some cases are not built correctly. Please check the log file for details.")
    sys.exit(1)