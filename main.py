from src.Compound import Compound, Control, Sample
from src.DataLoader import DataLoader
from src.Dataset import Dataset


def main():
    ALPHA = 0.05
    FOLDCHANGE = 1

    dataset = DataLoader().load_fragpipe("amp_lysis_test.tsv", "metadata copy.csv")

    # Preprocessing
    dataset.normalize()
    dataset.remove_incomplete_data()
    dataset.impute_simple()

    # Statistics
    dataset.prepare_analysis()
    dataset.ttest()

    dataset.foldchange()
    dataset.check_significance(ALPHA, FOLDCHANGE)

    dataset.save_results(ALPHA, FOLDCHANGE)


if __name__ == "__main__":
    main()
