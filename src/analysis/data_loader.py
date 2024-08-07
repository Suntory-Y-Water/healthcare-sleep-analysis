# data_loader.py
import pandas as pd
import xml.etree.ElementTree as ET

def load_sleep_data(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    sleep_data = []
    for record in root.findall('.//Record'):
        if record.get('type') == 'HKCategoryTypeIdentifierSleepAnalysis' and record.get('value') == 'HKCategoryValueSleepAnalysisInBed':
            start_date = record.get('startDate')
            end_date = record.get('endDate')
            source_name = record.get('sourceName')
            sleep_data.append([start_date, end_date, source_name])
    
    df = pd.DataFrame(sleep_data, columns=['Start', 'End', 'SourceName'])
    df['Start'] = pd.to_datetime(df['Start'])
    df['End'] = pd.to_datetime(df['End'])
    df['Duration'] = df['End'] - df['Start']
    
    return df

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