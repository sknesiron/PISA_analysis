from collections.abc import MutableSequence

from src.Compound import Control, Sample


class Dataset(MutableSequence):
    def __init__(self, *args):
        self._list: list[Sample] = list(args)
        self.controls: list[Control] = list()

    def __getitem__(self, index):
        return self._list[index]

    def __setitem__(self, index, value):
        self._list[index] = value

    def __delitem__(self, index):
        del self._list[index]

    def __len__(self):
        return len(self._list)

    def insert(self, index, value):
        self._list.insert(index, value)

    def __str__(self):
        return str(self._list)

    def __repr__(self):
        return repr(self._list)

    def add_control(self, control: Control):
        self.controls.append(control)

    def normalize(self):
        for ctrl in self.controls:
            ctrl.normalize()
        for sample in self._list:
            sample.normalize()

    def remove_incomplete_data(self):
        for ctrl in self.controls:
            ctrl.remove_incomplete_data()

        for sample in self._list:
            sample.remove_incomplete_data()

    def impute_simple(self):
        for ctrl in self.controls:
            ctrl.impute_simple()

        for sample in self._list:
            sample.impute_simple()

    def prepare_analysis(self):
        for sample in self._list:
            sample.prepare_analysis()

    def ttest(self):
        for sample in self._list:
            sample.ttest()

    def foldchange(self):
        for sample in self._list:
            sample.foldchange()

    def check_significance(self, alpha, foldchange):
        for sample in self._list:
            sample.check_significance(alpha=alpha, foldchange=foldchange)

    def save_results(self, alpha, foldchange):
        for sample in self._list:
            sample.plot_results(alpha=alpha, foldchange=foldchange)
            sample.save_results()
