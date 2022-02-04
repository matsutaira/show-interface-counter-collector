import re
import sys
import csv
import os
import configparser

def check_drop_count(logs):
    logs_int = re.findall(rf'{if_pattern}\s', logs)
    logs_drops = re.findall(rf'{check_pattern}', logs)
    logs_dict = dict(zip(logs_int, logs_drops))
    return logs_dict

def check_drop_if():
    first_log = re.search(rf'.*NTP,\s{dates[0]}[\s\S\n]*?.*#', show_log)
    last_log = re.search(rf'.*NTP,\s{dates[-1]}[\s\S\n]*?.*#', show_log)
    first_dict = check_drop_count(first_log.group())
    last_dict = check_drop_count(last_log.group())
    diff_dict = dict(last_dict.items() - first_dict.items())
    drop_if = sorted(diff_dict.keys())
    return drop_if

def collect_data(counter_regex, data):
    counts =[]
    for counter in data:
        count = re.findall(counter_regex, counter)
        counts += count
    return counts

def get_config():
    header = ['date']
    counter_regex = []
    for keys in ini['counter']:
        header.append(keys)
        counter_regex.append(ini['counter'][keys])
    return header, counter_regex

def generate_csv(interfaces):
    for interface in interfaces:
        if_name = interface.replace('/', '_')
        if_data = re.findall(rf'{interface}[\s\S\n]*?swapped\sout', show_log)
        if_count = []
        counts = []
        for regex in get_config()[1]:
            counts += [collect_data(rf'{regex}', if_data)]
        for i, date in enumerate(dates):
            if_count += [[date]]
            for n in range(len(get_config()[1])):
                if_count[i] += [counts[n][i]]
        with open(f'{file_name}_{if_name}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(get_config()[0])
            writer.writerows(if_count)
        f.close()
        print(f'generated file "{file_name}_{if_name}.csv"')

f = open(sys.argv[1], 'r')
ini = configparser.ConfigParser()
ini.read('show_interface_counter_collector.ini', encoding='UTF-8')

show_log = f.read()
check_pattern = ini['counter_checker']['pattern']
if_pattern = ini['if_checker']['pattern']

dates = re.findall(r'.*#show\sinterface[\s\S\n]*?NTP,\s(\d+:\d+:\d+.\d+.*)', show_log)

file_name = os.path.splitext(os.path.basename(sys.argv[1]))[0]

if __name__ == '__main__':
    try:
        if re.compile(if_pattern).search(sys.argv[2]):
            if_arg = [sys.argv[2]]
            generate_csv(if_arg)
            print("done")
        else:
            print("This IF name was not supported on this tool.")
            print("done")
    except IndexError:
        generate_csv(check_drop_if())
        print("done")
