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

change = {'RUN_REFDIR': '/cluster/work/users/herfugl/archive/n1850.ne16pg3_tn14.ppe_base_run.noresm3_b04._20251106/rest/0351-04-01-00000'}

bulk_xmlchange(cases, change)
