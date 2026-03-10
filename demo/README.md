# Demo

This notebook demonstrates homolog-search-tools functionality using ADH1, alcohol dehydrogenase, as a case study. The  workflow follows common computational analyses required for metabolic engineering.

1. Fetching sequence metadata from UniProt API.
2. Computing pairwise sequence similarities with BlastP and Diamond.
3. Visualizing sequences with sequence similarity networks (SSNs).

## Files

1. homolog_search_tools_Demo.ipynb: contains code for the analysis.
2. ADH1_UniProtKN-20260306: contains ADH1 accession ids from Swiss-Prot.


## Takeaways

For the ADH1 dataset, BlastP and Diamond return highly correlated sequence similarity scores with Diamond being approximately one order of magnitude faster (300ms vs 4000ms). Diamond is recommended for this workflow especially when analyzing large sets of sequences. The ADH1 sequence space is comprised of Eukaryota, more specifically Metazoa. Using SSNs we are able to identify four distinct clusters: a large zinc-binding alcohol dehydrogenase cluster with Metazoa and Viridiplantae sub-groups, a small Fungi cluster sharing the same PFAM annotations, a short-chain dehydrogenase cluster with Metazoa sequences, and an iron-containing alcohol dehydrogenase cluster with Fungi sequences.