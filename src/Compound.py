import os
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import ttest_ind
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import normalize


@dataclass
class Compound:
    file: str
    metadata: str
    name: str
    df: pd.DataFrame

    def to_numpy(self):
        return self.df.to_numpy()

    def from_numpy(self, array: np.array):
        self.df.loc[:] = array

    def normalize(self):
        self.df.loc[:] = normalize(self.df, norm="l1", axis=0).astype("float64")

    def impute_simple(self):
        self.df.replace(0, np.nan, inplace=True)
        imputer = SimpleImputer(
            missing_values=np.nan,
            strategy="constant",
            fill_value=self.df.min(axis=None),
        )
        self.df.loc[:] = imputer.fit_transform(self.df)


@dataclass
class Control(Compound):
    type = "control"

    def remove_incomplete_data(self):
        self.df.replace(0, np.nan, inplace=True)
        self.df.dropna(axis=0, thresh=2, inplace=True)
        self.df.replace(np.nan, 0, inplace=True)


@dataclass
class Sample(Compound):
    control: Control
    type = "sample"
    result: pd.DataFrame = field(default_factory=lambda: pd.DataFrame())

    @property
    def control_df(self):
        return self.control.df.loc[self.df.index].copy()

    def remove_incomplete_data(self):
        self.df.replace(0, np.nan, inplace=True)
        self.df = self.df.loc[self.control.df.index].dropna(axis=0, thresh=2)
        self.df.replace(np.nan, 0, inplace=True)

    def prepare_analysis(self):
        self.result = pd.concat([self.df, self.control_df], axis=1)
        self.result[f"{self.name}_mean"] = self.df.mean(axis=1)
        self.result[f"{self.control.name}_mean"] = self.control_df.mean(axis=1)

    def ttest(self):
        ttest_result = ttest_ind(self.df, self.control_df, axis=1)
        self.result["p-value"] = ttest_result.pvalue

        self.result["-log10_p-value"] = -np.log10(self.result["p-value"])
        return ttest_result

    def foldchange(self):
        self.result["log2foldchange"] = np.log2(
            self.result[f"{self.name}_mean"] / self.result[f"{self.control.name}_mean"]
        )

    def check_significance(self, alpha, foldchange):
        self.result["significant"] = (
            self.result["log2foldchange"].abs() >= foldchange
        ) & (self.result["p-value"] <= alpha)

    def plot_results(self, alpha, foldchange, ax=None):
        if ax is None:
            fig, ax = plt.subplots()

        df = self.result
        sns.set_theme(style="ticks")
        sns.scatterplot(
            data=df,
            x="log2foldchange",
            y="-log10_p-value",
            ax=ax,
            hue="significant",
            legend=False,
        )
        sns.despine(offset=10, trim=True)
        ax.hlines([-np.log10(alpha)], xmin=-3, xmax=3, ls="--", color="k")
        ax.vlines([-foldchange, foldchange], ymin=0, ymax=5, ls="--", color="k")
        ax.set(
            ylim=[0, df["-log10_p-value"].max() + 0.1],
            xlim=[df["log2foldchange"].min() - 0.5, df["log2foldchange"].max() + 0.5],
        )
        fig.suptitle(f"{self.name}", fontsize=10)
        fig.tight_layout()

    def save_results(self, folder):
        working_folder = Path(folder)
        main_result_folder = (
            working_folder
            / f"{datetime.today().strftime('%Y%m%d')}_{Path(self.file).stem}"
        )
        result_folder = (
            main_result_folder
            / f"{datetime.today().strftime('%Y%m%d')}_{self.name}_{self.control.name}"
        )

        if not os.path.isdir(main_result_folder):
            os.mkdir(main_result_folder)

        if not os.path.isdir(result_folder):
            os.mkdir(result_folder)

        plt.savefig(
            result_folder
            / f"{datetime.today().strftime('%Y%m%d')}_{self.name}_{self.control.name}_volcano_plot.svg",
            format="svg",
        )
        self.result.to_csv(
            result_folder
            / f"{datetime.today().strftime('%Y%m%d')}_{self.name}_{self.control.name}_results.csv"
        )
