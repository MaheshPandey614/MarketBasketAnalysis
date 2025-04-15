
# Core Libraries
import pandas as pd
import numpy as np

# Visualisation
import matplotlib.pyplot as plt
import seaborn as sns

# Market Basket Analysis
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# Graph Visualisation
import networkx as nx
# loading the data
data = pd.read_csv(r"C:\GitHub\MarketBasketAnalysis\Data\OnlineRetail.csv")

#EDA
print(data.info())
print(data.head())

#Count missing values per column
missing_values = data.isnull().sum()
print("Missing Values:\n", missing_values)

##Handling Credit Notes

# Identifying credit notes
credit_notes = data[data['InvoiceNo'].astype(str).str.startswith('C')].copy()
credit_notes.loc[:, 'OriginalInvoiceNo'] = credit_notes['InvoiceNo'].str[1:]

# Identifying original invoices related to credit notes
original_invoice_nos = credit_notes['OriginalInvoiceNo'].unique().tolist()

# Identifying credit note InvoiceNos
credit_note_invoice_nos = credit_notes['InvoiceNo'].unique().tolist()

# Identifying possible invalid transactions (not starting with 'C') that have negative quantity or missing/zero price
problematic_regulars = data[
    (~data['InvoiceNo'].astype(str).str.startswith('C')) &
    (
        (data['Quantity'] < 0) |
        (data['UnitPrice'].isnull()) |
        (data['UnitPrice'] == 0)
    )
]
problematic_regular_invoice_nos = problematic_regulars['InvoiceNo'].unique().tolist()

# Combining all invalid invoices to remove
all_invalid_invoice_nos = set(original_invoice_nos + credit_note_invoice_nos + problematic_regular_invoice_nos)


cleaned_data = data[~data['InvoiceNo'].isin(all_invalid_invoice_nos)]


#Cleaned data check¶

print("Cleaned dataset shape:", cleaned_data.shape)
print("Sample data:")
print(cleaned_data.head())

missing_values = cleaned_data.isnull().sum()
print("Missing Values:\n", missing_values)

print(cleaned_data.describe())

print("Unique Products:", cleaned_data['Description'].nunique())
print("Unique Invoices:", cleaned_data['InvoiceNo'].nunique())
print("Unique Customers:", cleaned_data['CustomerID'].nunique())
print("Countries:", cleaned_data['Country'].unique())


# Most popular products by quantity sold
top_products = cleaned_data['Description'].value_counts().head(10)
plt.figure(figsize=(12,6))
sns.barplot(y=top_products.index, x=top_products.values, hue=top_products.index, palette='viridis', legend=False)
plt.title('Top 10 Most Sold Products')
plt.xlabel('Quantity Sold')
plt.ylabel('Product Description')
plt.show()

#Number of transaction by countries

country_counts = cleaned_data['Country'].value_counts().head(10)

plt.figure(figsize=(12,6))
sns.barplot(y=country_counts.index, x=country_counts.values, hue=country_counts.index, palette='mako')
plt.title('Top 10 Countries by Number of Transactions')
plt.xlabel('Number of Transactions')
plt.ylabel('Country')
plt.show()


#Preparation for the MBA

# Group products by InvoiceNo to create basket-like structure
transactions = cleaned_data.groupby('InvoiceNo')['Description'].apply(list)

# Convert to list of lists for encoding
transactions_list = transactions.tolist()

# Preview
print("Sample transaction:\n", transactions_list[0])
print(f"\nTotal transactions prepared: {len(transactions_list)}")

#Encoder - creating encoded dataframe

te = TransactionEncoder()
te_ary = te.fit(transactions_list).transform(transactions_list)
transaction_df = pd.DataFrame(te_ary, columns=te.columns_)
transaction_df.head()

#Applying the Apriori
# Generate frequent itemsets
frequent_itemsets = apriori(transaction_df, min_support=0.02, use_colnames=True)

# Preview results
frequent_itemsets.sort_values(by='support', ascending=False).head(10)

#Generating rules

rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1.0) # Generate association rules from frequent itemsets

rules_sorted = rules.sort_values(by="lift", ascending=False) #sorting by the lift value
rules_sorted.head(10) #previewing the head

#Filtering rules

# Filter for high-confidence, high-lift rules
strong_rules = rules[(rules['lift'] > 1.2) & (rules['confidence'] > 0.5)]

# Preview top strong rules
strong_rules.sort_values(by='lift', ascending=False).head(10)


#Creating scatter plot of the rules

plt.figure(figsize=(10,6))
sns.scatterplot(data=rules, x="support", y="confidence", size="lift", hue="lift", palette="inferno_r", sizes=(50, 300))
plt.title("Association Rules: Support vs Confidence (Size = Lift)")
plt.xlabel("Support")
plt.ylabel("Confidence")
plt.legend(title="Lift", loc='upper right')
plt.tight_layout()
plt.show()


#Top rules by Lift

# Create a new column for the rule label

top10 = rules.sort_values(by='lift', ascending=False).head(10).copy()
top10['rule'] = top10['antecedents'].astype(str) + " → " + top10['consequents'].astype(str)

# Plot with rule as hue and disable legend
plt.figure(figsize=(12,6))
sns.barplot(
    y="rule", 
    x="lift", 
    hue="rule", 
    data=top10, 
    palette="magma", 
    legend=False
)
plt.title("Top 10 Association Rules by Lift")
plt.xlabel("Lift")
plt.ylabel("Rule")
plt.tight_layout()
plt.show()


#Association rules as a network graph

# creating a directed graph
G = nx.DiGraph()

# Just top 50 association rules being visualised sorted by by lift
sample_rules = rules.sort_values(by='lift', ascending=False).head(50)

# Adding edges between products with lift as weight
for _, row in sample_rules.iterrows():
    for antecedent in row['antecedents']:
        for consequent in row['consequents']:
            G.add_edge(antecedent, consequent, weight=row['lift'])

# Define layout
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, k=0.7, iterations=20)

# Nodes and edges
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='lightgreen')
nx.draw_networkx_edges(G, pos, width=1, edge_color='gray', arrows=True)
nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold')

# Adding title and turning off the axes
plt.title("Association Rules Network Graph (Top 50 by Lift)", fontsize=14, fontweight='bold')
plt.axis('off')
plt.tight_layout()
plt.show()
