from pathlib import Path
from tinkertool.scripts.create_ppe.config import BuildPPEConfig
from tinkertool.scripts.create_ppe.create_ppe import build_ppe

# Perform commands from the script directory pov
script_dir = Path(__file__).parent


buildppe_config = BuildPPEConfig(
  simulation_setup_path   = script_dir.joinpath('input_files', 'simulation_setup.ini').resolve(),
  build_base_only         = False,
  clone_only_during_build = True,
  keepexe                 = False,
  overwrite               = True,
  verbose                 = 2,
  log_dir                 = script_dir.joinpath('output_files', 'logs').resolve(),
  log_mode                = 'w'
)

build_ppe(buildppe_config)
