import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("final_data.csv")

# Overall correlation
corr, pvalue = stats.pearsonr(df["sentiment_delta"], df["stock_pct_change"])
print(f"Overall Pearson Correlation: {corr:.4f}")
print(f"P-value: {pvalue:.4f}")
print(f"Statistically significant: {pvalue < 0.05}")

# Per company correlation
print("\nPer company correlation:")
for company, group in df.groupby("company"):
    if len(group) > 3:
        r, p = stats.pearsonr(group["sentiment_delta"], group["stock_pct_change"])
        print(f"{company}: r={r:.4f}, p={p:.4f}")

# Scatter plot
plt.figure(figsize=(10, 6))
for company, group in df.groupby("company"):
    plt.scatter(group["sentiment_delta"], group["stock_pct_change"], label=company, alpha=0.7)

plt.axhline(y=0, color='black', linestyle='--', linewidth=0.8)
plt.axvline(x=0, color='black', linestyle='--', linewidth=0.8)
plt.xlabel("Sentiment Delta (QoQ Change in Positive Score)")
plt.ylabel("Stock Price Change % (1 day after earnings)")
plt.title(f"Sentiment Delta vs Stock Price Movement\nPearson r = {corr:.4f}, p = {pvalue:.4f}")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.savefig("correlation_plot.png", dpi=150)
plt.show()
print("\nPlot saved to correlation_plot.png")