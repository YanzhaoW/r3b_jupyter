import numpy as np
import pandas as pd
import ROOT


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

    def convert_to_dataframe(self, filepath: str, rename_map=None):
        data_arrays = ROOT.RDataFrame("evt", ROOT.TFile(filepath)).AsNumpy(self.branches)

        entry_size = self.__get_total_entries(data_arrays[self.branches[0]])
        columns = {branch: np.zeros(entry_size) for branch in self.branches}
        for column in columns.values():
            column[:] = np.nan
        columns["event_id"] = np.zeros(entry_size, dtype="int")

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
        data_frame = data_frame.astype(self.branches_types)
        if rename_map is not None:
            data_frame = data_frame.rename(columns=rename_map)
        return data_frame