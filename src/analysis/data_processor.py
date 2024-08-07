# data_processor.py
import pandas as pd

def calculate_sleep_metrics(df, start_date, end_date):
    # タイムゾーンを合わせる
    start_date = pd.to_datetime(start_date).tz_localize('Asia/Tokyo')
    end_date = pd.to_datetime(end_date).tz_localize('Asia/Tokyo')
    
    # 指定期間のデータをフィルタリング
    mask = (df['Start'] >= start_date) & (df['End'] <= end_date)
    period_df = df[mask]

    # 外れ値を除外
    period_df = remove_outliers(period_df, 'Duration')

    # 平均睡眠時間と中央値を計算
    mean_duration = period_df['Duration'].mean()
    median_duration = period_df['Duration'].median()
    
    return mean_duration, median_duration

def remove_outliers(df, column):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]