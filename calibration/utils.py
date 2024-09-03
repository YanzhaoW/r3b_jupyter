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


class RootPDConverter:
    def __init__(self, branches_types: dict[str, str]):
        self.branches_types = branches_types
    
    def __get_total_entries(self, obj_lists):
        entry = 0
        for obj_list in obj_lists:
            entry += len(obj_list)
        return entry
    

    @property
    def branches_types(self):
        return self._branches_types

    @property
    def branches(self):
        return self._branches

    @branches_types.setter
    def branches_types(self, branches_types: dict[str, str]):
        self._branches_types = branches_types
        self._branches = list(self._branches_types.keys())

    def convert_to_dataframe(self, path: str, folder: str = None):
        file_full_path = path
        if folder != None:
            file_full_path = f"{folder}/{path}"
        root_file = ROOT.TFile(file_full_path)
        data_arrays = ROOT.RDataFrame("evt", root_file).AsNumpy(self.branches)
    
        entry_size = self.__get_total_entries(data_arrays[self.branches[0]])
        columns = {branch : np.zeros(entry_size) for branch in self.branches}
        columns["event_id"] = np.zeros(entry_size, dtype = 'int')
        for column in columns.values():
            column = np.nan
            
        index: int = 0
        event_id: int = 0
        for objs_list in zip(*data_arrays.values()):
            for objs in zip(*objs_list):
                for branch, obj_value in zip(self.branches, list(objs)):
                    columns[branch][index] = obj_value
                    columns["event_id"][index] = event_id
                index += 1
            event_id += 1
        data_frame = pd.DataFrame(columns).dropna()
        return data_frame.astype(self.branches_types)