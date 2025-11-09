
class GeneExplainer:
    def summarize_gene(self, gene: str) -> str:
        # simplified deterministic text generator
        examples = {
            'INS': 'Encodes insulin hormone, regulating glucose metabolism.',
            'IL2RA': 'Alpha chain of interleukin-2 receptor, key in T-cell activation.',
            'PTPN22': 'Protein tyrosine phosphatase involved in autoimmunity regulation.'
        }
        return examples.get(gene, f'{gene} is a gene with limited functional annotation.')
