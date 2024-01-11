from datetime import datetime, timedelta
import csv

def read_input_file(file_name):
    file_path = f'./{file_name}'  # Assuming the CSV file is in the same directory as the script
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        data = list(reader)
    return data

def calculate_days_worked(employee_data):
    days_worked = set()
    for entry in employee_data:
        time_str = entry['Time']
        
        if not time_str:
            continue  # Skip entries with empty 'Time' field
        
        timestamp = datetime.strptime(time_str, '%m/%d/%Y %I:%M %p')
        day = timestamp.date()
        days_worked.add(day)
    return len(days_worked)


def analyze_work_hours(employee_data):
    consecutive_days = 0
    for i in range(1, len(employee_data)):
        curr = employee_data[i]
        prev = employee_data[i - 1]

        curr_time_in_str = curr['Time']
        prev_time_out_str = prev['Time Out']

        if not curr_time_in_str or not prev_time_out_str:
            continue  # Skip entries with empty 'Time' or 'Time Out' fields

        curr_time_in = datetime.strptime(curr_time_in_str, '%m/%d/%Y %I:%M %p')
        prev_time_out = datetime.strptime(prev_time_out_str, '%m/%d/%Y %I:%M %p')

        time_diff = curr_time_in - prev_time_out

        if 1 * 60 * 60 < time_diff.total_seconds() <= 10 * 60 * 60:
            consecutive_days += 1
        else:
            consecutive_days = 0

        if consecutive_days == 6:
            return True

    return False


def analyze_shift_hours(employee_data):
    for entry in employee_data:
        time_in_str = entry['Time']
        time_out_str = entry['Time Out']
        
        if not time_in_str or not time_out_str:
            continue  # Skip entries with empty 'Time' or 'Time Out' fields

        time_in = datetime.strptime(time_in_str, '%m/%d/%Y %I:%M %p')
        time_out = datetime.strptime(time_out_str, '%m/%d/%Y %I:%M %p')

        hours_worked = (time_out - time_in).total_seconds() / 3600

        if hours_worked > 14:
            return True

    return False


def main():
    file_name = 'input.csv'  # Adjust the file name as per your actual CSV file
    data = read_input_file(file_name)

    with open('output.txt', 'w') as output_file:
        for entry in data:
            name = entry['Employee Name']
            position = entry['Position ID']
            employee_data = [e for e in data if e['Employee Name'] == name]

            # a) Check for 7 consecutive days of work
            if calculate_days_worked(employee_data) == 7:
                output_file.write(f"{name}, {position}: Worked 7 consecutive days\n")

            # b) Check for less than 10 hours between shifts but greater than 1 hour
            if analyze_work_hours(employee_data):
                output_file.write(f"{name}, {position}: Less than 10 hours between shifts\n")

            # c) Check for more than 14 hours in a single shift
            if analyze_shift_hours(employee_data):
                output_file.write(f"{name}, {position}: Worked more than 14 hours in a single shift\n")

if __name__ == "__main__":
    main()
