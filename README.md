<div align="center">

<h1>BankMate - Smart Banking Bot Assistant</h1>
<p>
  A fast, lightweight, guidance-only banking chatbot<br>
  Built for Nigerian banks & fintechs • Fully customizable • No real actions performed
</p>

[![GitHub stars](https://img.shields.io/github/stars/apdoolhamza/BankMate-AI?style=social)](https://github.com/apdoolhamza/BankMate-AI/stargazers)
[![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.1-orange?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation PDF](https://img.shields.io/badge/📘%20Project_Documentation-PDF-blue)](https://github.com/apdoolhamza/BankMate-AI/blob/main/Project_Documentation.pdf)
[![Kaggle](https://kaggle.com/static/images/open-in-kaggle.svg)](https://www.kaggle.com/code/apdoolhamza/bankmate-ai-chatbot)
[![Live Demo on Hugging Face](https://img.shields.io/badge/🤗%20Live%20Demo-Hugging%20Face-yellow)](https://huggingface.co/spaces/apdoolhamza/BankMate-Bot)
</div>

## Features

- **Guidance-only** — explains procedures, never performs real banking actions  
- **13 banking intents** (balance check, transfer, lost card, loan, bills, airtime, fraud, complaints, USSD, ATM/branch, etc.)  
- **682+ unique training examples** — realistic Nigerian English + Pidgin  
- **12–15 natural responses per intent** — feels very human, never robotic  
- **Ultra-lightweight model** (\~300–800 KB) • < 5 ms inference • CPU-only  
- **Easy customization** — edit CSV (examples) or JSON (responses) in seconds  
- **Beautiful modern Gradio UI** — very responsive  
- **Insightful visualizations** — class distribution, word clouds, confusion matrix, top features, t-SNE  
- **Ready for production** — FastAPI / Docker templates

## Demo

[![Live Demo on Hugging Face](https://img.shields.io/badge/🤗%20Live%20Demo-Hugging%20Face-yellow)](https://huggingface.co/spaces/apdoolhamza/BankMate-Bot)

## Screenshots

<table>
  <tr>
    <td><img src="Images/UI 2.jpeg" width="100%" alt="Light mode chat"></td>
  </tr>
  <tr>
    <td colspan="2" align="center"><em>Modern chat UI with typing animation & natural replies</em></td>
  </tr>
</table>

<p align="center">
  <img src="Images/Distribution%20of%20training%20examples.png" width="45%" alt="Intent Distribution">
  <img src="Images/Confusion Matrix.png" width="45%" alt="Confusion Matrix">
</p>

<p align="center">
  <em>Class distribution & confusion matrix (generated during training)</em>
</p>

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/apdoolhamza/BankMate-AI/.git
cd BankMate-AI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the chatbot
python app.py
```
## Customization (No coding required)
Change responses (tone, Pidgin, bank name, etc.)
* Open ```bankmate_responses.json```
* Edit any list of replies
* Save → restart Gradio

## Add new intents or more examples
* Open ```bankmate_intents_data.csv``` in Excel / Google Sheets
* Add rows like this:
```
new_intent,how do I reset my password
new_intent,what to do if I forget PIN
```
* Save file
* Re-run training codes ```Notebook``` once

## Visualizations (Auto-generated during training)
* Intent distribution bar chart
* Word clouds (per intent)
* Confusion matrix heatmap
* Top contributing features per intent
* t-SNE semantic separation plot
All are in /images/ folder — perfect for reports or presentations.

## Tech Stack
* Core Model: scikit-learn (TF-IDF + Logistic Regression)
* Interface: Gradio (modern chat UI)
* Data: CSV (examples) + JSON (responses)
* Visualization: Matplotlib, Seaborn, WordCloud, t-SNE
* Model Saving: joblib

## License
MIT License – feel free to use, modify, and deploy commercially.

## Author

```
Apdoolmajeed Hamza (apdoolhamza)
AI/ML Engineer | Full-stack Web Developer
```
- LinkedIn: https://www.linkedin.com/in/apdoolhamza/
- GitHub:   https://github.com/apdoolhamza/

Star ⭐ the repo if you find it helpful!
