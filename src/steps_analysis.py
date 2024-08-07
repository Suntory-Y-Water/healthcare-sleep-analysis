from analysis.data_loader import load_sleep_data, load_steps_data
from analysis.data_processor import calculate_correlation
from analysis.data_plot import plot_correlation, plot_mode_distribution

def main():
    SLEEP_DATA_FILE_PATH = "./data/export.xml"
    
    # XMLデータを読み込み
    sleep_df = load_sleep_data(SLEEP_DATA_FILE_PATH)
    steps_df = load_steps_data(SLEEP_DATA_FILE_PATH)
    
    # 睡眠データと運動データの相関関係を計算
    correlation, merged_df = calculate_correlation(sleep_df, steps_df)
    print(f"睡眠時間と歩数の相関関係: {correlation}")

    # 相関関係の散布図を表示
    plot_correlation(merged_df)

    # 睡眠時間の最頻値を表示
    plot_mode_distribution(merged_df, 'Duration', 'Sleep Duration Mode Distribution')
    
    # 歩数の最頻値を表示
    plot_mode_distribution(merged_df, 'Steps', 'Steps Mode Distribution')

if __name__ == "__main__":
    main()
