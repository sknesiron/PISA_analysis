# PISA-analysis workflow

Simple workflow with GUI-inputs for analysis of PISA data from the Functional Metabolomics Lab.

## Data input:

1. `.tsv`-file -> Fragpipe output; Please name your samples in Fragpipe after the following scheme:

`<SAMPLENAME>_<REPLICATE_NR>` -> Examples: FirstSample_1, FirstSample_2, FirstSample_3, SecondSample_1, SecondSample_2, SecondSample_3

2. `.csv`-file -> Metadata input; the csv should have 3 columns named `Sample`, `Type`,`Control`

|Column Name|Description|
|---|---|
|Sample|Name of the Sample without its replicate number|
|Type|Either `Sample` or `Control` depending on wether the sample was used as a control or a sample|
|Control|Which sample from the sample column this sample should be compared to|

3. Fold-change -> Fold change between control to be considered significant
4. alpha-value -> threshold below which the p-value is seen as significant

## Output
1. Volcano plots for each sample
2. Table for each Sample summarizing the results