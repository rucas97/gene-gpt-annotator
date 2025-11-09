import pandas as pd
from tqdm import tqdm
from gene_explainer import GeneExplainer


def annotate_genes(gene_file: str) -> pd.DataFrame:
    """
    Reads input genes (one per line) and returns a DataFrame
    with explanations using GeneExplainer.
    """
    explainer = GeneExplainer()
    genes = []

    with open(gene_file, 'r') as infile:
        for line in infile:
            g = line.strip()
            if not g:
                continue
            genes.append(g)

    results = []
    for gene in tqdm(genes, desc="Annotating genes", ncols=80):
        desc = explainer.summarize_gene(gene)
        results.append({"Gene": gene, "Description": desc})

    return pd.DataFrame(results)
