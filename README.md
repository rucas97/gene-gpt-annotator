🧬 GeneGPT Annotator - Full README

AI‑assisted gene function annotator that generates concise gene summaries and functional category classifications, exporting both Markdown and HTML reports. Designed for reproducible offline genomic analysis and easy integration with Docker‑based pipelines.



🌟 Features

The GeneGPT Annotator is designed to bridge the gap between raw gene lists derived from high-throughput experiments (like GWAS studies or differential expression analyses) and actionable biological interpretation. It achieves this through automated functional summarization and standardized classification.

Automated Gene Summarization: The

The core feature revolves around retrieving a high-quality, concise functional summary for any given gene symbol.





Deterministic Stub: Currently, the system uses a deterministic function within gene_explainer.py. This stub serves as a placeholder for future, more complex generative models. For the current iteration, specific known genes map to pre-defined, authoritative descriptions to ensure immediate utility and reproducibility without external network dependencies.



Future LLM Integration: The architecture is explicitly designed to easily swap the deterministic stub for a true Large Language Model (LLM) backend. This upgrade path, detailed in the technical roadmap, will utilize models such as those from HuggingFace Transformers or OpenAI/Anthropic APIs to provide context-aware, dynamic summaries based on the latest literature or user-specified model parameters.

Ontology‑Based Classification

To facilitate rapid categorization of gene sets, the annotator employs a simplified, keyword-driven ontology matcher (ontology_matcher.py). This ensures that even without complex semantic parsing, genes can be grouped into high-level functional buckets relevant to common areas of biomedical research.

The primary classification categories are:





Immune Regulation: Genes associated with T-cell signaling, cytokine pathways, MHC complexes, or autoimmune disease associations.



Metabolic: Genes involved in primary catabolic or anabolic pathways, lipid processing, or glucose homeostasis.



General Function: Genes coding for structural proteins, general transcription factors, or those whose function is not strictly defined within the other two categories for the current system configuration.

The matching process relies on an internal dictionary mapping known functional keywords to these categories. The scoring mechanism uses a simple count of matching terms found in the gene summary.

Multi‑Format Reporting

Reproducibility and presentation are paramount. The tool generates outputs suitable for both programmatic pipeline integration and human-readable reports:





Markdown Report (results/report.md): Ideal for integration into documentation, GitHub READMEs, or simple text-based reporting systems. It presents the data in a clean, standard GitHub Flavored Markdown table.



HTML Report (results/report.html): Generated using the jinja2 templating engine. This output provides a fully styled, ready-to-view table, often incorporating light CSS for better readability, suitable for direct embedding into lab electronic lab notebooks (ELNs) or supplementary materials for publications.

Fully Offline Operation

The system is engineered for environments where constant network access or API key management is restricted or undesirable (e.g., secure computing clusters, fieldwork). All data processing, lookups, and report generation occur locally on the host machine or within the specified Docker container.

Containerized Build

A dedicated Dockerfile ensures that the exact environment—including Python version, installed libraries, and system dependencies (if any)—is perfectly preserved, eliminating "it works on my machine" issues. This is crucial for collaborative bioinformatics workflows.



🧠 Project Architecture

The project structure is designed for modularity, separating the core logic, I/O handling, and presentation layers.

gene-gpt-annotator/
├── data/
│   └── example_genes.txt          # Example input gene list (User provides this)
├── src/
│   ├── main.py                    # Orchestrator: Reads input, calls workers, triggers reporting.
│   ├── variant_annotator.py       # Wrapper handling file I/O for gene lists and integrating explainer/matcher.
│   ├── gene_explainer.py          # Core logic for summarizing gene functions (Currently the deterministic AI stub).
│   ├── ontology_matcher.py        # Keyword-based classification logic for biological categories.
│   ├── report_generator.py        # Utilizes pandas and jinja2 to render Markdown and HTML reports.
│   └── __init__.py                # Makes the 'src' directory a Python package.
├── Dockerfile                     # Defines the reproducible container environment.
├── requirements.txt               # Lists all necessary Python packages (pandas, jinja2, tqdm).
├── README.md                      # This documentation file.
└── results/                       # Auto‑generated output directory (intentionally kept out of Git version control via .gitignore).


Component Breakdown:





main.py: The entry point. It manages the workflow sequence: read genes $\rightarrow$ annotate $\rightarrow$ classify $\rightarrow$ save raw data $\rightarrow$ generate reports.



gene_explainer.py: The most critical component regarding future scalability. It houses the mapping mechanism for functional descriptions. In the current state, it might look something like this internally: [ \text{Function}(\text{Gene}) = \begin{cases} \text{"Insulin production and glucose regulation."} & \text{if Gene} = \text{'INS'} \ \text{"T-cell signaling and autoimmune susceptibility."} & \text{if Gene} = \text{'IL2RA'} \ \text{...} & \text{otherwise} \end{cases} ]



ontology_matcher.py: This module processes the output string from the GeneExplainer. It scans for predefined keywords (e.g., "T-cell," "cytokine," "insulin," "lipid," "transcription factor") and assigns the highest scoring category.



report_generator.py: Leverages pandas to structure the results data frame and jinja2 to inject this structure into HTML templates.



⚙️ Installation

Two primary methods are supported, depending on whether you prefer the isolation of Docker or direct local installation.

Option 1 — Docker (recommended, fully isolated)

Using Docker ensures that dependency conflicts are avoided and the environment is identical across all execution platforms.





Build the Image: Navigate to the root directory of the project and execute the build command. This creates a local image tagged gene-gpt-annotator.

docker build -t gene-gpt-annotator .




Run the Annotation Pipeline: Execute the container. The critical part here is the volume mount (-v ${PWD}:/app), which maps the current working directory (where your data/ folder resides) into the container's working directory (/app). This allows the input file to be read and the output files to be written back to your host machine.

# Assumes you are in the root directory containing Dockerfile and data/
docker run --rm -v ${PWD}:/app gene-gpt-annotator






--rm: Automatically removes the container instance after it exits.



-v ${PWD}:/app: Mounts the current local directory to /app inside the container.

Option 2 — Native (Python ≥ 3.9)

If you prefer not to use Docker, you can set up a standard Python virtual environment.





Create and Activate Virtual Environment:

python -m venv venv
# On Linux/macOS
source venv/bin/activate
# On Windows (Command Prompt)
venv\Scripts\activate.bat
# On Windows (PowerShell)
venv\Scripts\Activate.ps1




Install Dependencies: Ensure you have requirements.txt in the root directory.

pip install -r requirements.txt




Execute the Script: Run the main orchestrator script.

python src/main.py




📤 Input Format

The GeneGPT Annotator requires a simple, standardized input file containing only the identifiers to be processed.





File Type: Plain text (.txt).



Structure: One gene symbol per line. No headers, no extra columns, no special characters (unless they are part of the official symbol, e.g., certain rodent gene nomenclature).

Example (data/example_genes.txt):

INS
IL2RA
PTPN22
BRCA1
CYP2D6
TP53
TNF


This simple format allows for easy integration with shell scripts or custom analysis pipelines that generate gene lists.



📄 Output

Execution completes by writing three artifacts to the results/ directory. Before running, ensure this directory exists or that the script has permission to create it.

1. Raw Data ()

A standard comma-separated values file, ideal for subsequent computational analysis, visualization using external tools (like R or Excel), or importing into databases.

Columns: GeneSymbol, Summary, Category, KeywordsFound.

2. Markdown Report ()

A human-readable summary table using standard Markdown syntax.

Example Snippet:

# GeneGPT Annotation Report
## Date: 2025-10-27

| Gene Symbol | Summary | Category | Keywords Found |
| :--- | :--- | :--- | :--- |
| INS | Essential hormone for glucose homeostasis. | Metabolic | hormone, glucose, metabolism |
| IL2RA | A subunit of the interleukin-2 receptor, critical for T-cell homeostasis. | Immune Regulation | T-cell, cytokine, receptor, immune |
...


3. HTML Report ()

A richly formatted report using embedded CSS styles for presentation quality.

Example Console Output Snippet:

Annotating genes: 100%|██████████| 7/7 [00:00<00:00, 15.32it/s]
✅ Annotated 7 genes successfully.
🧬 Annotations saved → results/annotated_genes.csv
✅ Markdown report generated → results/report.md
📄 HTML report generated → results/report.html




🧩 Technical Stack

A detailed breakdown of the technologies employed:

ComponentTechnologyRationaleLanguagePython 3.12Modern features, strong library support for bioinformatics.Data HandlingpandasRobust and efficient manipulation of tabular data structures.Progress TrackingtqdmProvides clear, dynamic progress bars for iterative tasks.Templatingjinja2Powerful, secure, and flexible engine for generating HTML/Markdown.ContainerizationDocker 24+Ensures environmental consistency and portability.AI Core (current)Deterministic GeneExplainer stubGuarantees offline functionality and baseline output consistency.Planned UpgradeHuggingFace Transformers / LLM APIsAllows transition to true AI-driven functional summarization.



📘 Example Use Case: Post-GWAS Prioritization

Imagine a recent Genome-Wide Association Study (GWAS) has identified 50 novel loci associated with Type 2 Diabetes (T2D). The associated genes are extracted, resulting in a list of 65 unique symbols.

Workflow with GeneGPT Annotator:





Input Preparation: The 65 gene symbols are compiled into data/my_t2d_genes.txt.



Execution: The Docker image is run, mounting the current directory.



Analysis: The resulting results/report.md is immediately reviewed. Researchers can quickly filter the list:





Genes flagged as Metabolic (e.g., INS, PPARGC1A) receive immediate high priority due to direct pathway relevance.



Genes flagged as Immune Regulation (e.g., CTLA4, PTPN22) are prioritized for investigation into potential immune-mediated inflammation components of T2D pathology.



Integration: The annotated_genes.csv is imported into a statistical environment for correlation testing against expression data from relevant immune and metabolic tissues.

This rapid, reproducible process minimizes the time spent on manual literature review for initial triage.



🧑‍💻 Author

Reza Anvaripour (rucas97) — MSc Molecular Genetics

Driven by the need for reproducible bioinformatics tools that bridge the gap between wet-lab data and accessible computational summaries.

📧 rez.anvaripour@gmail.com
🔗 github.com/rucas97



🪪 License

This project is distributed under the MIT License.



Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:





The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.



THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

Feel free to fork, modify, and distribute with attribution.



🤝 Contributions

Contributions are highly valued, especially in areas that enhance the tool's core functionality and versatility.

Key Areas for Improvement:





AI Model Integration (gene_explainer_ai.py): Development of robust wrapper functions for integrating modern, localized generative models (e.g., running flan-t5-large or quantized versions of newer models locally via HuggingFace pipelines). Performance benchmarking against remote APIs (like GPT-4o-mini) is welcome.



Ontology Mapping Refinement: Expanding the keyword dictionary in ontology_matcher.py to cover broader biological domains (e.g., Neurobiology, Developmental Biology) and implementing more sophisticated term weighting or fuzzy matching.



Report Visualization Enhancements: Improving the report_generator.py templates to include basic interactivity (e.g., sorting in the HTML table via JavaScript libraries like DataTables) or better styling for mobile viewing.

Please open an Issue to discuss large feature requests before submitting a Pull Request.



🧭 Citation

If this tool, or concepts derived from it, significantly contribute to your research or analysis leading to a publication, please cite the repository:



Anvaripour R. (2025). GeneGPT Annotator: Lightweight Offline AI‑Assisted Gene Function Annotator.
GitHub Repository: https://github.com/rucas97/gene-gpt-annotatore-gpt-annotator)
