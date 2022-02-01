import numpy as np
import pandas as pd
from os.path import dirname, join, isfile
from os import listdir
import re
import threading
from typing import List

pmu_filename_prog = re.compile(r'^.*_([0-9]{4})([0-9]{2})([0-9]{2})([0-9]{2})\.csv$')

class InvalidCSVError(Exception):
    pass

class UnknownPMUName(Exception):
    pass

def get_pmu_date(dir_path, pmu_name):
    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    for file in files:
        if pmu_name in file:
            result = pmu_filename_prog.match(file)
            year = result.group(1)
            month = result.group(2)
            day = result.group(3)
            hour = result.group(4)
            return year, month, day
    raise UnknownPMUName
         

def read_file(file_path, timestamp_col_num, freq_col_num):
    '''
    timestamp_col_num and freq_col_num are zero based indices.
    '''
    try:
        file_data = pd.read_csv(
            file_path,
            usecols=[timestamp_col_num, freq_col_num],
            #dtype={timestamp_col_num: np.datetime64, freq_col_num: np.float32},
            dtype={freq_col_num: np.float32},
            parse_dates=[timestamp_col_num],
            infer_datetime_format=True, # this speeds things up
            #date_parser=pd.to_datetime # this slows things down
            index_col=timestamp_col_num,
            squeeze=True # to return a series
        )
    except IndexError:
        raise InvalidCSVError

    #file_data.rename(columns=lambda name: 'Frequency' if 'FREQ' in name else name, inplace=True)
    #file_data.name = 'Frequency'
    print(f'Finished reading file: "{file_path}"')
    return file_data


def read_pmu_day(dir_path: str, pmu_name: str, year: str, month: str, day: str,
             timestamp_col_num: int, freq_col_num: int):
    print(f'Reading PMU data for {pmu_name}')
    day_data = []
    for hour in range(24):
        hour = f'{hour:02}'
        file_name = pmu_name + '_' + year + month + day + hour + '.csv'
        file_path = join(dir_path, file_name)
        hour_data = read_file(file_path, timestamp_col_num, freq_col_num)
        hour_data.name = pmu_name
        day_data.append(hour_data)
        print(f'Retrieved hour: {hour}')
    # Then need to concat all these into the same dataframe
    arr = pd.concat(day_data)
    print(f'Finished concatenating PMU data for: {pmu_name}')
    return arr


def read_pmu_hour(dir_path: str, pmu_name: str, year: str, month: str, day: str,
                  hour: str, timestamp_col_num: int, freq_col_num: int):
    print(f'Reading PMU data for {pmu_name}')
    file_name = pmu_name + '_' + year + month + day + hour + '.csv'
    file_path = join(dir_path, file_name)
    hour_data = read_file(file_path, timestamp_col_num, freq_col_num)
    hour_data.name = pmu_name
    return hour_data


def read_day(dir_path, pmu_names, timestamp_col, freq_col):
    for pmu_name in pmu_names:
        try:
            year, month, day = get_pmu_date(dir_path, pmu_name)
        except UnknownPMUName:
            print(f'PMU "{pmu_name}" does not exist.')
        else:
            print(f'Date: {day}/{month}/{year}')
            break
    
    series_list = []
    for pmu_name in pmu_names:
        print(f'Begin retrieving data for PMU: {pmu_name}')
        pmu_data = read_pmu_day(dir_path, pmu_name, year, month, day, 0, 3)
        series_list.append(pmu_data)
    
    df = pd.concat(series_list, axis=1, keys=[s.name for s in series_list])
    print('Finished loading in data for day')
    return df


def threaded_read_day(dir_path, pmu_names, timestamp_col, freq_col):
    for pmu_name in pmu_names:
        try:
            year, month, day = get_pmu_date(dir_path, pmu_name)
        except UnknownPMUName:
            print(f'PMU "{pmu_name}" does not exist.')
        else:
            print(f'Date: {day}/{month}/{year}')
            break
    
    series_list = [None] * len(pmu_names)
    threads: List[threading.Thread] = []
    i = 0
    def exec_read_pmu(index, pmu_name):
        series_list[index] = read_pmu_day(dir_path, pmu_name, year, month, day, 0, 3)
    for pmu_name in pmu_names:
        print(f'Begin retrieving data for PMU: {pmu_name}')
        thr = threading.Thread(target=exec_read_pmu, args=(i, pmu_name))
        thr.start()
        threads.append(thr)
        i += 1

    i = 0
    for thr in threads:
        thr.join()

    df = pd.concat(series_list, axis=1, keys=[s.name for s in series_list])
    print('Finished loading in data for day')
    return df


def read_hour(dir_path, pmu_names, hour, timestamp_col, freq_col):
    for pmu_name in pmu_names:
        try:
            year, month, day = get_pmu_date(dir_path, pmu_name)
        except UnknownPMUName:
            print(f'PMU "{pmu_name}" does not exist.')
        else:
            print(f'Date: {day}/{month}/{year}')
            break
    
    series_list = []
    for pmu_name in pmu_names:
        print(f'Begin retrieving data for PMU: {pmu_name}')
        pmu_data = read_pmu_hour(dir_path, pmu_name, year, month, day, hour, 0, 3)
        series_list.append(pmu_data)
    
    df = pd.concat(series_list, axis=1, keys=[s.name for s in series_list])
    print('Finished loading in data for day')
    return df
    

def read_gps(file_path):
    gps_data = pd.read_excel(
        file_path,
        index_col=0,
        usecols='B:D',
        names=['Name', 'Latitude', 'Longitude'],
        dtype={'Name': str, 'Latitude': np.float32, 'Longitude': np.float32}
    )
    return gps_data


def test_read_file():
    try:
        file = read_file('D:\\PMU\\2021\\07\\28\\Ecblue04_2021072800.csv', 0, 3)
    except InvalidCSVError:
        print('could not read csv')
    print(file)
    print(file.dtypes)
    print('done')


def test_get_pmu_date():
    try:
        year, month, day = get_pmu_date('D:\\PMU\\2021\\07\\28', 'Ecblue04')
    except UnknownPMUName:
        print('pmu name not available')
        return
    print(f'Year: {year}')
    print(f'Month: {month}')
    print(f'Day: {day}')


def test_read_pmu_day():
    year, month, day = get_pmu_date('D:\\PMU\\2021\\07\\28', 'Ecblue04')
    pmu_data = read_pmu_day('D:\\PMU\\2021\\07\\28', 'Ecblue04', year, month, day, 0, 3)
    print(pmu_data)
    print(type(pmu_data))


def test_read_pmu_hour():
    year, month, day = get_pmu_date('D:\\PMU\\2021\\07\\28', 'Ecblue04')
    hour = '00'
    hour_data = read_pmu_hour('D:\\PMU\\2021\\07\\28', 'Ecblue04', year, month, day, hour, 0, 3)
    print(hour_data)
    

def test_read_day():
    day_data = read_day('D:\\PMU\\2021\\07\\28', ['Ecblue04', 'Ecblue0203'], 0, 3)
    print(day_data)


def test_read_hour():
    hour_data = read_hour('D:\\PMU\\2021\\07\\28', ['Ecblue04', 'Ecblue0203'], '00', 0, 3)
    print(hour_data)


def test_threaded_read_day():
    day_data = threaded_read_day('D:\\PMU\\2021\\07\\28', ['Ecblue04', 'Ecblue0203'], 0, 3)
    print(day_data)


def test_read_gps():
    gps_data = read_gps('D:\\PMU\\PMU_GPS.xlsx')
    print(gps_data)


if __name__ == '__main__':
    #test_read_file()
    #test_get_pmu_date()
    #test_read_pmu_day()
    #test_read_pmu_hour()
    #test_read_day()
    test_read_hour()
    #test_read_gps()
    #test_threaded_read_day()