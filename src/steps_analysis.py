import pandas as pd
import xml.etree.ElementTree as ET
from sleep_analysis import load_sleep_data

def load_steps_data(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    steps_data = []
    for record in root.findall('.//Record'):
        if record.get('type') == 'HKQuantityTypeIdentifierStepCount':
            date = record.get('startDate')
            steps = record.get('value')
            steps_data.append([date, steps])
    
    df = pd.DataFrame(steps_data, columns=['Date', 'Steps'])
    df['Date'] = pd.to_datetime(df['Date'])
    df['Steps'] = df['Steps'].astype(int)
    
    return df

def calculate_correlation(sleep_df, steps_df):
    # 日付ごとに睡眠データを集約
    sleep_df['Date'] = sleep_df['Start'].dt.date
    daily_sleep = sleep_df.groupby('Date')['Duration'].sum().reset_index()
    
    # 日付ごとに運動データを集約
    steps_df['Date'] = steps_df['Date'].dt.date
    daily_steps = steps_df.groupby('Date')['Steps'].sum().reset_index()
    
    # 睡眠データと運動データを結合
    merged_df = pd.merge(daily_sleep, daily_steps, on='Date')
    
    # 相関関係を計算
    correlation = merged_df['Duration'].corr(merged_df['Steps'])
    
    return correlation

def main():
    SLEEP_DATA_FILE_PATH = "./data/export.xml"
    
    # XMLデータを読み込み
    sleep_df = load_sleep_data(SLEEP_DATA_FILE_PATH)
    steps_df = load_steps_data(SLEEP_DATA_FILE_PATH)
    
    # 睡眠データと運動データの相関関係を計算
    correlation = calculate_correlation(sleep_df, steps_df)
    print(f"睡眠時間と歩数の相関関係: {correlation}")

if __name__ == "__main__":
    main()
