# homolog-search-tools

Python-based module to search protein databases for homologs, visualize search results, and perform sequence-based analysis for downstream applications. 
 
**Explore gene sequence space:** Visualize sequence space using sequence similarity networks (SSNs) with pairwise sequence similarities computed with `homolog_search_tools.similarity` functions to identify sequence clusters with UniProt metadata 
fetched with `homolog_search_tools.search`.

## Features
- Retrieve metadata from UniProt REST API
- Compute pairwise sequence similarities
- FileIO with FASTA files

## Installation
```bash
pip install git+https://github.com/chrisnguyen11/homolog-search-tools.git
```

## Quick Start
- `UniProtRequest`: a class that interacts with the UniProt REST API
- `BlastP`: a class that wraps the command-line ncbi-blast+ program 

```python
import pandas as pd
from homolog_search_tools.search import UniProtRequest
from homolog_search_tools.similarity import BlastP

# Fetch sequence metadata from UniProt
accessions = ["A0A2U1LIM9","P10127"]
uniprot_api = UniProtRequest({email})
records = uniprot_api.fetch_records(accessions)

# Run BlastP to find homologs
sequence_df = pd.DataFrame([
    {"Header": "P05067", "Sequence": "MLPGLALLLL"},
    {"Header": "Q28757", "Sequence": "SEVKMDAEFR"}]
)
blastp = BlastP()
blastp_output = blastp.run_allvsall(sequence_df)
```

## Install Third-Party Tools 
Refer to this [Dockerfile](https://github.com/chrisnguyen11/homolog-search-tools/tree/main/Dockerfile) for setting up a Jupyter environment with ncbi-blast+, diamond, mmseqs2, and clustalo.

## Example
- Refer to the [demo](https://github.com/chrisnguyen11/homolog-search-tools/tree/main/demo) to explore a set of ADH1 protein sequences using several homolog-search-tools functions.
- Check out  [protein-language-modeling](https://github.com/chrisnguyen11/protein-language-modeling) for a larger project using homolog-search-tools functions in the context of protein language modeling.

## Testing
Executes within the homolog_search_tools directory to run unitest on common functions.

```bash
python -m pytest  
```