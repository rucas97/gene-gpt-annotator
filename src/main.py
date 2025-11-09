import os
import pandas as pd
from tqdm import tqdm
from variant_annotator import annotate_genes
from report_generator import build_reports


def main(gene_file: str):
    """
    Entry point for GeneGPT Annotator.
    Reads genes, annotates them, exports CSV, and generates reports.
    """
    os.makedirs("results", exist_ok=True)

    print(f"Annotating genes from: {gene_file}")
    df = annotate_genes(gene_file)
    print(f"✅ Annotated {len(df)} genes successfully.\n")

    csv_path = os.path.join("results", "annotated_genes.csv")
    df.to_csv(csv_path, index=False)
    print(f"🧬 Annotations saved → {csv_path}")

    build_reports(csv_path)


if __name__ == "__main__":
    gene_file = "data/example_genes.txt"
    main(gene_file)
