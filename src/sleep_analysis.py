from analysis.data_loader import load_sleep_data
from analysis.data_processor import calculate_sleep_metrics
import pandas as pd

def main():
    DATA_FILE_PATH = "./data/export.xml"
    
    # XMLデータを読み込み
    df = load_sleep_data(DATA_FILE_PATH)
    
    # ニート期間の睡眠データを計算
    neet_start = pd.to_datetime('2021-04-01')
    neet_end = pd.to_datetime('2021-10-31')
    neet_mean, neet_median = calculate_sleep_metrics(df, neet_start, neet_end)
    
    # 社会人期間の睡眠データを計算
    work_start = pd.to_datetime('2023-11-22')
    work_end = pd.to_datetime('2024-06-21')
    work_mean, work_median = calculate_sleep_metrics(df, work_start, work_end)
    
    print(f"ニート期間の平均睡眠時間: {neet_mean}")
    print(f"ニート期間の睡眠時間の中央値: {neet_median}")
    print(f"社会人期間の平均睡眠時間: {work_mean}")
    print(f"社会人期間の睡眠時間の中央値: {work_median}")

if __name__ == "__main__":
    main()
