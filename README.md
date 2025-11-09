# GeneGPT Annotator

Standalone AI-powered gene functional annotator. Summarizes gene functions and classifies them into categories, producing Markdown and HTML reports.

Author: Reza Anvaripour (rucas97)
License: MIT

Usage:

docker build -t gene-gpt-annotator .
docker run --rm -v ${PWD}:/app gene-gpt-annotator
