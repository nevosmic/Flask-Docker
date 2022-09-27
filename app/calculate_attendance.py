import pandas as pd
import jellyfish
import os
import sys
import datetime
import itertools
import operator

# csv columns headers columns:
ROOM_NAME = "Meeting Name"
ROOM_START = "Meeting Start Time"
ROOM_FINISH = "Meeting End Time"
NAMES = "Name"
EMAILS = "Attendee Email"
JOIN_TIME = "Join Time"
JOIN_TIME_NUM = 5
LEAVE_TIME = "Leave Time"
LEAVE_TIME_NUM = 6
OVERALL_TIME = "Attendance Duration"
PLATFORM = "Connection Type"


def get_csv_list(fetched_list):
    """
    calculates a list containing all participants csv data - each list came from one csv file (single Webex meeting)
    :param fetched_list: tuples list of all csv file's data that came from database
    :return: a list of lists of tuples of all participants Webex data
    """

    # list of lists of tuples : [[(Meeting Name,Meeting Start Time,Meeting End Time...),(Meeting Name...)],[()]]
    list_of_meetings = []
    # Group by Meeting Start Time
    for key, group in itertools.groupby(fetched_list, operator.itemgetter(1)):
        list_of_meetings.append(list(group))

    if len(list_of_meetings) == 0:
        print("There is no participant's meetings files!")
        exit(1)
    return list_of_meetings


def get_data(meeting_data):
    """
    analyzes the data from a list created from a Webex meeting and returning it as a pd.DataFrame
    :param csv_data: list of tuples
    :return: pd.DataFrame sorted by the join times and the maximal overall login time in the file
    """
    # create DataFrame using csv data
    df = pd.DataFrame(meeting_data, columns=[ROOM_NAME, ROOM_START, ROOM_FINISH, NAMES, EMAILS, JOIN_TIME, LEAVE_TIME, OVERALL_TIME, PLATFORM])
    # calculate maximal overall login time in the file:
    df.sort_values(by=[LEAVE_TIME], ascending=False, inplace=True)  # descending order by leave time
    latest = str(df.iloc[0, LEAVE_TIME_NUM]).rsplit(" ")[1]     # take first row after sort
    latest_hour = int(latest.rsplit(":")[0])
    latest_min = int(latest.rsplit(":")[1])
    df.sort_values(by=[JOIN_TIME], ascending=True, inplace=True)    # ascending order by join time
    earliest = str(df.iloc[0, JOIN_TIME_NUM]).rsplit(" ")[1]  # take first row after sort
    earliest_hour = int(earliest.rsplit(":")[0])
    earliest_min = int(earliest.rsplit(":")[1])
    max_overall = (latest_hour - earliest_hour) * 60 + (latest_min-earliest_min)

    return df, max_overall


def init(fetched_list):
    """
    initiates all parameters that are needed for the script: the dictionary of the participants, list of csv data lists
    and the initiative pd.DataFrame
    :return: pd.DataFrame, list of csv data and the dictionary of the participants
    """
    time_dict = {}
    csv_list = get_csv_list(fetched_list)
    init_data, m = get_data(csv_list[0])
    dict_init(init_data, time_dict)
    df = pd.DataFrame(index=time_dict.keys())

    return df, csv_list, time_dict


def check_spell(df_email, time_dict):
    """
    the function checks if an email is misspelled by up to several errors
    if so, then the function returns the correct one, else, the function returns false
    :param df_email: string of an email from the DataFrame
    :param time_dict: dictionary of participants
    :return: String or void
    """
    for mail in time_dict.keys():
        if jellyfish.damerau_levenshtein_distance(df_email, mail) < 3:
            return mail
    return


def check_hebrew(s):
    """
    checks if a string contains any hebrew letter, if so returns true, else returns false
    :param s: string
    :return: bool
    """
    for c in s:
        if ord('\u05d0') <= ord(c) <= ord('\u05ea'):    # if the character is in range of the unicode of hebrew letters
            return True
    return False


def dict_init(df, time_dict):
    """
    initiates the participant's dictionary for every Webex meeting
    :param df: pd.DataFrame
    :param time_dict: dictionary of the participants
    """
    # initializing all keys:
    for username in time_dict.keys():
        time_dict[username]['time'] = []
        time_dict[username]['overall'] = 0

    for i, row in df.iterrows():
        file_email = str(row[EMAILS])
        username = file_email.rsplit('@')[0]
        if "bynet" in file_email or "8200" in file_email or "nan" in file_email:  # skipping the non-students
            continue
        file_name = str(row[NAMES])
        if not check_spell(username, time_dict):  # if the mail is not already in the dictionary- add it
            time_dict[username] = {'time': [], 'overall': 0, 'name': file_name}
        else:   # if it is then update it
            username = check_spell(username, time_dict)   # correcting
            if not check_hebrew(file_name):   # if the name in the file is not in hebrew
                # if there is a more accurate name let's update it
                if len(time_dict[username]['name']) < len(file_name):
                    time_dict[username]['name'] = file_name
                # if the dictionary's name is in hebrew, and we have an english name we should update it to be english
                if check_hebrew(time_dict[username]['name']):
                    time_dict[username]['name'] = file_name


def dict_update(email, time_dict, start, end, overall):
    """
    Formats the inputs: start and end times to a single string "start time - end time".
    calculates the overall login time.
    Updates the dictionary with the given values
    :param email: string
    :param time_dict: dictionary - {email : {time, overall}}
    :param start: string login time
    :param end: string logout time
    :param overall: string overall logged in time
    """
    time_dict[email]['time'].append(start.rsplit(' ')[1] + " - " + end.rsplit(' ')[1])
    time_dict[email]['overall'] += int(overall.replace(' mins', ''))


def dict_build(df, time_dict):
    """
    Building the dictionary based on the input
    :param df: DataFrame - input's data-frame
    :param time_dict:
    """
    dict_init(df, time_dict)
    for index, row in df.iterrows():
        file_email = str(row[EMAILS])
        file_name = row[NAMES]
        username = file_email.rsplit('@')[0]
        if time_dict.get(username):  # if the email is spelled correctly then it is in the dictionary
            dict_update(username, time_dict, row[JOIN_TIME], row[LEAVE_TIME], row[OVERALL_TIME])
        elif "bynet" in file_email or "8200" in file_email or "nan" in file_email or "Call-in User_2" in file_name:  # skipping the non-students:
            continue
        else:
            # checking if is misspelled and correcting it:
            username = check_spell(username, time_dict)
            if username:  # if such email exists then consider it as a misspelled email
                dict_update(username, time_dict, row[JOIN_TIME], row[LEAVE_TIME], row[OVERALL_TIME])
    special_cases(time_dict)
    return time_dict


def special_cases(time_dict):
    """
    checks for special cases in the login time frames
    :param time_dict: dictionary - {email : {time, overall}}
    """
    for mail in time_dict.keys():
        times = time_dict[mail]['time']
        if len(times) < 2:
            continue
        special = False
        # checking for a special case in logging times:
        i = 0
        while i + 1 < len(times):  # while a next time frame exists
            start = times[i].rsplit(' - ')[0]  # take first login time
            end = times[i].rsplit(' - ')[1]  # take first logout time
            start1 = times[i + 1].rsplit(' - ')[0]  # take second login time
            end1 = times[i + 1].rsplit(' - ')[1]  # take second logout time
            if end >= end1:  # it means, that user was logged in from several devices
                del (times[i + 1])
                special = True
            elif start1 <= end <= end1:  # if the logged time frames overlap then take the longest frame
                times[i] = start + " - " + end1
                del (times[i + 1])
                special = True
            else:
                i += 1

        if special:  # if a special case occurred, calculate the correct overall logged time
            overall = 0
            for frame in times:
                sh = int(frame.rsplit(":")[0])  # starting hour
                sm = int(frame.rsplit(":")[1])  # starting minute
                eh = int(frame.rsplit(":")[2].rsplit("- ")[1])  # ending hour
                em = int(frame.rsplit(":")[3])  # ending minute

                overall += (eh - sh) * 60 + (em - sm)
            time_dict[mail]['overall'] = overall


def add_csv(meeting_data, time_dict, new_overall):
    """
    adding every meeting data as a new column and analyzing it
    :param meeting_data: list of tuples
    :param time_dict: dictionary
    :param new_overall: new pd.DataFrame for the overall login time
    :return: the new pd.DataFrame of the overall login time
    after adding the column. also returning the maximum login time in the file
    """
    df, max_time = get_data(meeting_data)

    # adding values to dictionary:
    dict_build(df, time_dict)
    # building the new rows dictionaries:
    overall_dict = {}
    for mail in time_dict.keys():
        overall = time_dict[mail]['overall']
        overall_dict[mail] = overall
    file_date = str(df.iloc[0, JOIN_TIME_NUM]).rsplit(" ")[0]
    if file_date in new_overall.columns:    # if a meeting has several files than add
        for i, row in new_overall.iterrows():
            overall_dict[i] += row[file_date]

    new_overall = add_col(new_overall, file_date, overall_dict)
    return new_overall, max_time


def add_col(df, col_name, time_dict):
    """
    adding a column to a pd.DataFrame.
    :param df: pd.DataFrame
    :param col_name: string of the date of the file
    :param time_dict: dictionary of login time per user
    :return:
    """
    df = pd.DataFrame(df, index=time_dict.keys())   # updating the indexes to be up-to-date with all files
    df[col_name] = df.index.map(time_dict)
    return df


def add_names(df, time_dict):
    """
    add the updated names to the second row of the DataFrame
    :param df: pd.DataFrame
    :param time_dict: dictionary of names
    :return:
    """
    names = {}
    for key in time_dict.keys():
        names[key] = time_dict[key]['name']

    names_col = df.index.map(names)
    df.insert(loc=0, column='names', value=names_col)
    return df


def add_avg_and_total_time(df, sum_max):
    """
    adds an average time row and a total time row to the end of the DataFrame
    :param df: pd.DataFrame
    :param sum_max: sum of maximum time of every row
    :return: pd.DataFrame
    """
    sum_row = pd.DataFrame(df.sum(axis=1, numeric_only=True))
    sum = {}
    avg = {}
    i = 0
    for idx in df.index:
        av = round((sum_row.iloc[i, 0] / sum_max) * 100)
        avg[idx] = str(av)+ " %"
        sum[idx] = str(round(sum_row.iloc[i, 0]))
        i += 1
    df['average'] = df.index.map(avg)
    df['total time'] = df.index.map(sum)
    return df


def filter_db_fetch(db_fetch):
    """
    Convert datetime values to string and remove id
    :param db_fetch: fetched records from database list of tuples
    :return: new_db_fetch: processed fetched records
    """
    new_db_fetch = []
    for record in db_fetch:
        new_record = ()
        for val in record:
            if type(val) is datetime.datetime:
                new_record = new_record + (val.strftime("%m-%d-%Y %H:%M:%S"),)
            else:
                new_record = new_record + (val,)
        new_db_fetch.append(new_record[1:])
    return new_db_fetch


def calculate_attendance(db_fetch):
    """
        Creates a csv file with student's attendance statistics (based by Webex meeting data ONLY)
        :param db_fetch: fetched records from database list of tuples
    """
    new_db_fetch = filter_db_fetch(db_fetch)
    new_df, csv_files, init_dict = init(new_db_fetch)

    sum_maxes = 0
    for csv in csv_files:
        new_df, max_row = add_csv(csv, init_dict, new_df)
        sum_maxes += max_row
    new_df.sort_index(axis=1, inplace=True)
    new_df = add_avg_and_total_time(new_df, sum_maxes)
    new_df = add_names(new_df, init_dict)
    new_df.to_csv("not_final_output.csv")
    final_df = pd.concat([new_df.iloc[:, 0:1], new_df.iloc[:, -2:]], axis=1)
    print("DONE!!!")
    final_df.to_csv('attendance_output.csv')


if __name__ == '__main__':

    '''
    demo_db_fetch = [(1496, "Avichay Har Tov's Personal Room", datetime.datetime(2022, 9, 21, 15, 45, 31),
                 datetime.datetime(2022, 9, 21, 20, 6, 10), 'gal frylich', 'galfrylich@gmail.com',
                 datetime.datetime(2022, 9, 21, 16, 8, 23), datetime.datetime(2022, 9, 21, 16, 11, 17), '3',
                 'Mobile app'), (1497, "Avichay Har Tov's Personal Room", datetime.datetime(2022, 9, 21, 15, 45, 31),
                                 datetime.datetime(2022, 9, 21, 20, 6, 10), 'Yossi Bengaev', 'yossibenga@gmail.com',
                                 datetime.datetime(2022, 9, 21, 19, 8, 49), datetime.datetime(2022, 9, 21, 19, 9, 52),
                                 '2', 'Desktop app'), (1498, "Avichay Har Tov's Personal Room", datetime.datetime(2022, 9, 22, 15, 45, 31),
                                 datetime.datetime(2022, 9, 22, 20, 6, 10), 'Keren', 'Keren@gmail.com',
                                 datetime.datetime(2022, 9, 22, 19, 8, 49), datetime.datetime(2022, 9, 22, 19, 9, 52),
                                 '2', 'Desktop app')]
    '''
    calculate_attendance(db_fetch)



