# On the Identification of Self-Admitted Technical Debt with Large Language Models

## Overview

This repository contains the artifacts for the paper titled "On the Identification of Self-Admitted Technical Debt with Large Language Models". The paper investigates the performance of various large language models (LLMs) in identifying technical debt within issues from different software repositories. The artifacts include the code, data, and results that were used and generated during the study.

## Paper

The full version of the paper is available in this repository. You can access it [here](./artifacts/paper.pdf).

## Repository Structure

```plaintext
./
├── README.md                  # This file
├── LICENSE                    # MIT License
├── artifacts/                 # Folder containing all artifacts related to the paper
│   ├── paper.pdf              # Final version of the paper
│   ├── requirements.txt       # List of Python dependencies
│   ├── scripts/               # Folder containing the Python scripts used in the study
│   │   ├── llmAdapter.py      # Python class for interacting with LLM APIs
│   │   ├── PromptGenerator.py # Python class for storing and managing prompts
│   │   └── main_gen_study.py  # Main script for running the study
│   └── data/                  # Folder containing the datasets and results
│       ├── all_issues.csv     # All issues used in the study concatenated into a single file
│       ├── apache_traffic_TD_dataset.csv   # Dataset from apache_traffic
│       ├── owncloud_TD_dataset.csv         # Dataset from owncloud
│       ├── ubc_thunder_TD_dataset.csv      # Dataset from ubc_thunder
│       ├── va_gov_debt_TD_dataset.csv      # Dataset from va_gov
│       └── results_{{DATASET}}/            # Folder containing results for each dataset
```

## Requirements

To reproudce the study, you need the following dependencies installed:
```bash
pip install google-generativeai
pip install openai
pip install langchain langchain-core langsmith langchain_experimental
pip install langgraph langchain-community langchainhub grandalf
pip install anthropic langchain-anthropic
``` 
Ensure that you have API keys for OpenAI, Claude, and Google, as they are required by the scripts.

## Instalation and usage

1. Clone this repo:
```bash
git clone <repository-url>
cd <repository-folder>
```

2. Install Dependencies:
Make sure you have Python installed. Then install the required dependencies:
```bash
pip install -r artifacts/requirements.txt
```

3. Setup your API keys in the llmAdapter script
4. On the main script for the study, you can configure the dataset/llm/max_output_tokens/prompt_type to your liking
5. Run the script with
```bash
cd ./artifacts/scripts
python3 ./main_gen_study.py
```

## Data
The artifacts/data folder contains all the datasets used in the study:
- all_issues.csv: Contains every issue used in the study, along with labels indicating whether it is considered technical debt or not.
- apache_traffic_TD_dataset.csv, owncloud_TD_dataset.csv, ubc_thunder_TD_dataset.csv, va_gov_debt_TD_dataset.csv: Contain issues from specific repositories, as described in the paper.

Results for each LLM and prompt combination are saved in separate CSV files within the results_{{DATASET}} folders.

## Contact
For any questions or issues regarding this repository, please contact any of the authors at:
- pedro.lambert@sga.pucminas.br
- lucila@pucminas.br
- laertexavier@pucminas.br

**Affiliation:** Pontifical Catholic University of Minas Gerais (PUC Minas), Bachelor in Software Engineering.