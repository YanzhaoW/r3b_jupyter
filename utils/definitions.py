import pandas as pd
import numpy as np

def to_data_frame(root_file, cycle_offset):
    max_cycle_num = root_file.GetKey("NeulandHitPar",9999).GetCycle() 
    cycle_num = max_cycle_num + cycle_offset
    cal2hit_par = root_file.Get(f"NeulandHitPar;{cycle_num}")
    module_pars = cal2hit_par.GetListOfModulePar()
    size = len(module_pars)
    print(f"size of module pars: {size}")
    data_frame = pd.DataFrame({"bar_id": np.arange(1, size + 1), "t_diff": np.zeros(size), "t_diff_error": np.zeros(size), "effective_speed": np.zeros(size), "effective_speed_error": np.zeros(size), "t_sync": np.zeros(size),"t_sync_error": np.zeros(size)})
    for module_num, value in module_pars:
        module_id = module_num - 1
        data_frame.loc[module_id, "t_diff"] = value.tDiff.value
        data_frame.loc[module_id, "t_diff_error"] = value.tDiff.error
        data_frame.loc[module_id, "effective_speed"] = value.effectiveSpeed.value
        data_frame.loc[module_id, "effective_speed_error"] = value.effectiveSpeed.error
        data_frame.loc[module_id, "t_sync"] = value.tSync.value
        data_frame.loc[module_id, "t_sync_error"] = value.tSync.error
    return data_frame