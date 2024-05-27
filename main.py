import os
import sys
from collections.abc import MutableSequence
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import easygui
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import ttest_ind
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import normalize

from src.Compound import Control, Sample
from src.DataLoader import DataLoader
from src.Dataset import Dataset


def main():

    frag_pipe_tsv = easygui.fileopenbox(
        "Please select your fragpipe output", "Fragpipe Output", filetypes="tsv"
    )
    metadata_csv = easygui.fileopenbox(
        "Please select your metdata file", "Metadata", filetypes="csv"
    )

    user_input = easygui.multenterbox(
        "Select desired values:", "User-Input", ["Fold-change", "alpha"], [1, 0.05]
    )
    ALPHA = float(user_input[1])
    FOLDCHANGE = float(user_input[0])

    dataset = DataLoader().load_fragpipe(frag_pipe_tsv, metadata_csv)

    # Preprocessing
    dataset.normalize()
    dataset.remove_incomplete_data()
    dataset.impute_simple()

    # Statistics
    dataset.prepare_analysis()
    dataset.ttest()

    dataset.foldchange()
    dataset.check_significance(ALPHA, FOLDCHANGE)

    for sample in dataset:
        sample.plot_results(ALPHA, FOLDCHANGE)
        plt.show()

    folder_name = easygui.diropenbox(
        "Select the directory to save your data in", "Save Results"
    )
    dataset.save_results(ALPHA, FOLDCHANGE, folder_name)


if __name__ == "__main__":
    main()
