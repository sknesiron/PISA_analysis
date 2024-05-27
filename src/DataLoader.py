import sys
from pathlib import Path

import pandas as pd

from src.Compound import Control, Sample
from src.Dataset import Dataset


class DataLoader:
    def extract_compoundlist(self, df):
        return set([i.split("_")[0] for i in df.filter(like="MaxLFQ").columns])

    def load_metadata(self, filepath):
        if not Path(filepath).is_file() and Path(filepath).suffix == ".csv":
            print("Wrong filetype for metadata... Please use '.csv' files. Exiting...")
            sys.exit()
        else:
            df = pd.read_csv(filepath)
            return df

    def prepare_metadata(self, df):
        meta_dict = {}
        for control in df.Control.unique():
            meta_dict[control] = [
                row.Compound for i, row in df.iterrows() if row.Control == control
            ]
        return meta_dict

    def get_metadata(self, filepath):
        df = self.load_metadata(filepath)
        return self.prepare_metadata(df)

    def load_fragpipe(
        self, filepath_sample, filepath_metadata, datacolumns="MaxLFQ Intensity"
    ):

        meta_dict = self.get_metadata(filepath_metadata)

        if (
            not Path(filepath_sample).is_file()
            and Path(filepath_sample).suffix == ".tsv"
        ):
            print(
                "Wrong filetype for sample data... Please use '.tsv' files. Exiting..."
            )
            sys.exit()

        df = pd.read_table(filepath_sample)
        df.set_index("Protein ID", inplace=True)
        df = df.filter(regex=datacolumns).copy()
        df.rename(lambda x: x.replace(" MaxLFQ Intensity", ""), axis=1, inplace=True)

        dataset = Dataset()
        for ctrl, compounds in meta_dict.items():
            curr_control = Control(
                file=filepath_sample,
                metadata=filepath_metadata,
                name=ctrl,
                df=df.filter(regex=ctrl).copy().astype("float64"),
            )
            dataset.add_control(curr_control)
            for compound in compounds:
                dataset.append(
                    Sample(
                        file=filepath_sample,
                        metadata=filepath_metadata,
                        name=compound,
                        df=df.filter(regex=f"{compound}_").copy().astype("float64"),
                        control=curr_control,
                    )
                )
        return dataset
