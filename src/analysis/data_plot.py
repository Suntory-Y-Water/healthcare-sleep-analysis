import matplotlib.pyplot as plt
import seaborn as sns
from analysis.data_processor import remove_outliers

def plot_correlation(merged_df):
    # 睡眠時間を時間単位に変換（元データが秒単位の場合）
    merged_df['Duration'] = merged_df['Duration'].dt.total_seconds() / 3600  # 秒から時間に変換

    # 外れ値を除去
    merged_df = remove_outliers(merged_df, 'Duration')
    merged_df = remove_outliers(merged_df, 'Steps')

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Steps', y='Duration', data=merged_df)
    plt.title('Correlation between Sleep Duration and Steps')
    plt.xlabel('Steps')
    plt.ylabel('Sleep Duration (hours)')
    plt.show()

def plot_mode_distribution(df, column, title):
    mode_value = df[column].mode()[0]
    plt.figure(figsize=(10, 6))
    sns.histplot(df[column], kde=False, bins=30)
    plt.axvline(mode_value, color='r', linestyle='--', label=f'Mode: {mode_value}')
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.legend()
    plt.show()