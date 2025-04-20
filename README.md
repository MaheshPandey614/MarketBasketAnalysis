# 🛒 Market Basket Analysis

This project performs Market Basket Analysis on retail transaction data using association rule mining. The goal is to uncover frequently purchased product combinations and derive actionable insights using the Apriori algorithm.

---

## 📌 Objectives

- Clean and prepare transactional retail data.
- Structure data into basket format for analysis.
- Apply the Apriori algorithm to identify frequent itemsets.
- Generate association rules based on support, confidence, and lift.
- Visualise strong product relationships.

---

## 🗂️ Repository Structure

📂 MarketBasketAnalysis

├── 📂 Data (Datasets in excel, csv formats along with the project generated data for the reusability)

├── 📂 Python (Scripts for data processing & visualisation .ipnyb and .py files)

├── 📜 README.md (Project documentation)

---

## 🛠️ Tools & Libraries

- **Python**
- **Pandas**, **NumPy**
- **mlxtend** (for Apriori and association rules)
- **Seaborn**, **Matplotlib**
- **NetworkX** (for visualizing rules as a graph)

---

## Key Steps

1. Clean raw data: remove credit notes and related invoices, zero-priced rows, and inconsistencies.
2. Prepare transaction lists grouped by InvoiceNo.
3. Use the Apriori algorithm to extract frequent itemsets.
4. Generate and visualise association rules (support, confidence, lift).
5. Export final datasets and visuals for reuse and presentation.

---

## 🔁 Reproducibility

All cleaned and generated data files are saved in the `Data/` folder for reusability.

---

## 📊 Outputs

- Rules with high confidence and lift for product bundling.
- Visuals (bar plots, scatter plots, network graphs) to support business recommendations.

---

## ✅ Status

✔️ Completed  
---
