import os
import pandas as pd
from jinja2 import Template


def build_reports(csv_path: str, output_dir: str = "results"):
    """
    Create both Markdown and HTML reports for annotated genes.
    Args:
        csv_path (str): Path to annotated gene CSV file.
        output_dir (str): Directory to save reports (default: results).
    """
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_path)

    # Clean text safely for both Markdown & HTML contexts
    df = df.fillna("")
    for col in df.columns:
        df[col] = (
            df[col].astype(str)
            .str.replace("|", "−", regex=False)
            .str.replace("\n", " ", regex=False)
        )

    # ---------- Markdown ----------
    md_path = os.path.join(output_dir, "report.md")
    with open(md_path, "w", encoding="utf-8") as md:
        md.write("# GeneGPT Annotator Report\n\n")
        md.write(f"**Total genes:** {len(df)}\n\n")
        try:
            md.write(df.to_markdown(index=False))
        except Exception:
            # Fallback if tabulate is missing in environment
            md.write(df.to_string(index=False))
    print(f"✅ Markdown report generated → {md_path}")

    # ---------- HTML via Jinja2 ----------
    html_template = Template(
        """<!DOCTYPE html>
<html>
<head>
<meta charset='utf-8'/>
<title>GeneGPT Annotator Report</title>
<style>
body {font-family: Arial, sans-serif; margin: 20px;}
table {border-collapse: collapse; width: 100%;}
th, td {border: 1px solid #ddd; padding: 8px;}
th {background-color: #f2f2f2;}
</style>
</head>
<body>
<h2>GeneGPT Annotator Report</h2>
<p>Total genes analyzed: {{ count }}</p>
<table>
<tr>{% for c in cols %}<th>{{ c }}</th>{% endfor %}</tr>
{% for row in rows %}
<tr>{% for c in cols %}<td>{{ row[c] }}</td>{% endfor %}</tr>
{% endfor %}
</table>
</body>
</html>"""
    )

    html = html_template.render(
        count=len(df), cols=df.columns, rows=df.to_dict(orient="records")
    )
    html_path = os.path.join(output_dir, "report.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"📄 HTML report generated → {html_path}")
