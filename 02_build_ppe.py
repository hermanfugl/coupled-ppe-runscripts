from pathlib import Path
from tinkertool.scripts.create_ppe.config import BuildPPEConfig
from tinkertool.scripts.create_ppe.create_ppe import build_ppe

buildppe_config = BuildPPEConfig(
  simulation_setup_path = Path('/cluster/projects/nn9560k/johannef/NorESM_workdir/cases-test_tinkertool4coupled/run_scripts/input_files/simulation_setup.ini').resolve(),
  build_base_only       = False,
  clone_only_during_build = False,
  keepexe               = False,
  overwrite             = True,
  verbose               = 2,
  log_dir               = Path(f'/cluster/projects/nn9560k/johannef/NorESM_workdir/cases-test_tinkertool4coupled/run_scripts/output_files/logs').resolve(),
  log_mode              = 'w'
)

build_ppe(buildppe_config)
