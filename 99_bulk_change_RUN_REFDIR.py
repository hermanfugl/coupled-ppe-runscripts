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

change = {'RUN_REFDIR': '/cluster/projects/nn9560k/adagj/ppe_restfiles/'}

bulk_xmlchange(cases, change)
