#%%
# --- import modules ---
import xarray as xr
from pathlib import Path

from tinkertool.scripts.generate_paramfile.config import ParameterFileConfig
from tinkertool.scripts.generate_paramfile.generate_paramfile import generate_paramfile
from tinkertool.scripts.generate_paramfile.visualize_paramfile import visualize_paramfile

# Perform commands from the script directory pov
script_dir = Path(__file__).parent

#%%
# --- define parameter file configuration ---
parm_conf = ParameterFileConfig(
    param_ranges_inpath=script_dir.joinpath('input_files', 'NorESM3_tuningparameterinfo_PPE.ini').resolve(),
    param_sample_outpath=script_dir.joinpath('input_files', 'NorESM3_tuningparameterinfo_PPE_test.nc').resolve(),
    chem_mech_file=None,
    ctsm_default_param_file=Path('/cluster/shared/noresm/inputdata/lnd/clm2/paramdata/ctsm60_params.250923_v26j.nc'),
    fates_default_param_file=Path('/cluster/shared/noresm/inputdata/lnd/clm2/paramdata/fates_params_api.40.0.0_14pft_c250923_noresm_v26i.nc'),
    nmb_sim=3,
    avoid_scramble=False,
    exclude_default=False,
    log_dir=Path('/cluster/projects/nn9560k/johannef/NorESM_workdir/cases-test_tinkertool4coupled/run_scripts/output_files/logs'),
    verbose=2
)

#%%
# --- generate parameter file ---
generate_paramfile(config=parm_conf)

with xr.open_dataset(parm_conf.param_sample_outpath.with_suffix('.raw.nc')) as ds:
    ds_string = ds.to_dataframe().to_string()
print("\n", ds_string)

#%%
# --- visualize parameter file ---

visualize_paramfile(
    parm_conf.param_sample_outpath.with_suffix('.raw.nc'),
    save_path=Path('/cluster/projects/nn9560k/johannef/NorESM_workdir/cases-test_tinkertool4coupled/run_scripts/output_files/figures/NorESM3_tuningparameterinfo_PPE_test_pairplot.png'),
)

# %%
