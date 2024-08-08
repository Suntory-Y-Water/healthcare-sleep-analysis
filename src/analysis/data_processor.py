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

def calculate_correlation(sleep_df, steps_df):
    # 日付ごとに睡眠データを集約
    sleep_df['Date'] = sleep_df['Start'].dt.date
    daily_sleep = sleep_df.groupby('Date')['Duration'].sum().reset_index()
    
    print(daily_sleep)
    # 日付ごとに運動データを集約
    steps_df['Date'] = steps_df['Date'].dt.date
    daily_steps = steps_df.groupby('Date')['Steps'].sum().reset_index()
    
    # 睡眠データと運動データを結合
    merged_df = pd.merge(daily_sleep, daily_steps, on='Date')
    
    # 相関関係を計算
    correlation = merged_df['Duration'].corr(merged_df['Steps'])
    
    return correlation, merged_df

def remove_outliers(df, column):
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

def is_holiday(date, country_holidays):
    # 金曜日(4)と土曜日(5)が休日とする
    return date in country_holidays or date.weekday() in [4, 5]

def calculate_holiday_sleep_metrics(df, start_date, end_date, country_holidays):
    # タイムゾーンを合わせる
    start_date = pd.to_datetime(start_date).tz_localize('Asia/Tokyo')
    end_date = pd.to_datetime(end_date).tz_localize('Asia/Tokyo')
    
    # 指定期間のデータをフィルタリング
    mask = (df['Start'] >= start_date) & (df['End'] <= end_date)
    period_df = df[mask]
    
    # 日付ごとの休日フラグを追加
    period_df['IsHoliday'] = period_df['Start'].apply(lambda x: is_holiday(x, country_holidays))
    
    # 休日の睡眠データをフィルタリング
    holiday_sleep_df = period_df[period_df['IsHoliday']]
    
    # 休日の平均睡眠時間と中央値を計算
    mean_duration = holiday_sleep_df['Duration'].mean()
    median_duration = holiday_sleep_df['Duration'].median()
    
    return mean_duration, median_duration