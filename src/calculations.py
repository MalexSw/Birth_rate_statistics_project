import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats

def clean_and_plot_birth_counts(birth_counts):
    mean = birth_counts.mean()
    std = birth_counts.std()
    birth_counts_no_outliers = birth_counts[
        (birth_counts > mean - 3 * std) &
        (birth_counts < mean + 3 * std)
    ]

    birth_counts_log = np.log1p(birth_counts_no_outliers)
    plt.figure(figsize=(10, 6))
    plt.hist(birth_counts_log, bins=30, density=True, alpha=0.6, color='skyblue', edgecolor='black')
    mu, sigma = birth_counts_log.mean(), birth_counts_log.std()
    x = np.linspace(min(birth_counts_log), max(birth_counts_log), 100)
    plt.plot(x, stats.norm.pdf(x, mu, sigma), color='red')

    plt.title('Histogram of Cleaned & Log-Transformed Birth Counts')
    plt.xlabel('Log(Number of Births)')
    plt.ylabel('Density')
    plt.grid(True)
    plt.show()

    print(f"Mean (after cleaning and log transform): {mu:.4f}")

def birth_counts(birth_counts):
    sample_std = birth_counts.std(ddof=1)
    sample_mean = birth_counts.mean()
    n = len(birth_counts)
    confidence_level = 0.95
    alpha = 1 - confidence_level
    z_score = stats.norm.ppf(1 - alpha / 2)
    margin_of_error = z_score * (sample_std / np.sqrt(n))
    ci_lower = sample_mean - margin_of_error
    ci_upper = sample_mean + margin_of_error

    print(f"Sample Mean: {sample_mean:.2f}")
    print(f"Sample Standard Deviation: {sample_std:.2f}")
    print(f"Sample Size: {n}")
    print(f"{confidence_level*100:.0f}% Confidence Interval for the Mean: ({ci_lower:.2f}, {ci_upper:.2f})")

    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))

    count, bins, _ = plt.hist(birth_counts, bins=30, density=True, alpha=0.6, color='mediumseagreen', edgecolor='black')

    x = np.linspace(0, 2_000_000, 1000)  
    p = stats.norm.pdf(x, sample_mean, sample_std)
    plt.plot(x, p, 'k--', linewidth=2, label='Normal Distribution')

    plt.axvline(sample_mean, color='blue', linestyle='--', linewidth=2, label=f'Mean: {sample_mean:.0f}')

    ci_left = max(ci_lower, 0)
    ci_right = min(ci_upper, 2_000_000)
    plt.axvspan(ci_left, ci_right, color='skyblue', alpha=0.3, label='95% CI')

    plt.xlim(0, 2_000_000)

    plt.title('Histogram of Birth Counts with Normal Curve', fontsize=16)
    plt.xlabel('Number of Births', fontsize=12)
    plt.ylabel('Density', fontsize=12)
    plt.xticks(fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend()
    plt.tight_layout()
    plt.show()

def weightOverYears(births_per_year):
    plt.figure(figsize=(10, 6))
    plt.plot(births_per_year.index, births_per_year.values, marker='o', linestyle='-', color='blue')

    plt.title('Total Number of Births Over Years')
    plt.xlabel('Year')
    plt.ylabel('Number of Births')
    plt.grid(True)
    plt.xticks(births_per_year.index, rotation=45)
    plt.tight_layout()
    plt.show()

def top10Countries(birth_counts_by_country):
    top_10 = birth_counts_by_country.sort_values(ascending=False).head(10)

    plt.figure(figsize=(12, 6))
    plt.bar(top_10.index, top_10.values, color='skyblue', edgecolor='black')
    plt.title('Top 10 Countries by Number of Births')
    plt.xlabel('Country')
    plt.ylabel('Number of Births')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    
def countriesComparing(df, countriesForCompare):
    filtered = df[df['geo'].isin(countriesForCompare)]

    grouped = filtered.groupby('geo')['OBS_VALUE'].sum().sort_values(ascending=False)

    # Plotting
    plt.figure(figsize=(12, 6))
    plt.bar(grouped.index, grouped.values, color='skyblue', edgecolor='black')
    plt.title('Selected Countries by Total Birthes')
    plt.xlabel('Country')
    plt.ylabel('Total Birthes')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

def check_mean_difference(df, metric, group_col, group1, group2, alternative="two-sided", alpha=0.05):
    data1 = df[df[group_col] == group1][metric].dropna()
    data2 = df[df[group_col] == group2][metric].dropna()

    t_stat, p_value = stats.ttest_ind(data1, data2, alternative=alternative)

    plot_df = df[df[group_col].isin([group1, group2])][[metric, group_col]].dropna()
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=group_col, y=metric, data=plot_df, hue=group_col, palette="Set2", legend=False)
    plt.title(f"Comparison of '{metric}' Between {group1} and {group2}\n"
                  f"t={t_stat:.2f}, p={p_value:.4f}, significant={p_value < alpha}")
    plt.xlabel(group_col)
    plt.ylabel(metric)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    return {
        "group1_mean": data1.mean(),
        "group2_mean": data2.mean(),
        "t_statistic": t_stat,
        "p_value": p_value,
        "significant": p_value < alpha,
        "alpha": alpha
    }
    

def interpret_result(result):
    if result["significant"]:
        return f"✅ Statistically significant (p = {result['p_value']:.4f} < α = {result['alpha']}). Reject the null hypothesis."
    else:
        return f"❌ Not statistically significant (p = {result['p_value']:.4f} ≥ α = {result['alpha']}). Fail to reject the null hypothesis."