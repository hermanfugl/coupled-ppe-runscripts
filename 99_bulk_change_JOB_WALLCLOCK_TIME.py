from pathlib import Path
from tinkertool.scripts.create_ppe.create_ppe import bulk_xmlchange

script_dir = Path(__file__).parent

#collect all paths
cases = []
cases_dir = script_dir.parent
for case in cases_dir.iterdir():
    if case.is_dir():
        if 'ensemble_member' in case.name:
            cases.append(case)

cases.sort(key=lambda x: x.name)

change = {
    'JOB_WALLCLOCK_TIME': {
        'case.run': '15:00:00',
        'case.st_archive': '10:00:00',
        'case.compress': '18:00:00'
    }
}

bulk_xmlchange(cases, change)
