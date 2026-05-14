import re
import pandas as pd


def preprocess(data):

    # Supports:
    # 18/06/2024, 9:09 am -
    # 18/06/24, 21:09 -
    # 06/18/24, 9:09 PM -
    # 06/18/2024, 21:09 -

    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?(?:AM|PM|am|pm))?\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    dates = [d.replace("\u202f", " ") for d in dates]
    dates = [d.strip() for d in dates]

    df = pd.DataFrame({
        'user_message': messages,
        'message_date': dates
    })

    # Flexible datetime parsing
    df['message_date'] = pd.to_datetime(
        df['message_date'],
        dayfirst=True,
        errors='coerce',
        format='mixed'
    )

    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []

    for message in df['user_message']:

        entry = re.split(r'([^:]+?):\s', message)

        if len(entry) > 2:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages

    df.drop(columns=['user_message'], inplace=True)

    # Feature extraction
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Heatmap period column
    period = []

    for hour in df['hour']:

        if hour == 23:
            period.append("23-00")

        elif hour == 0:
            period.append("00-1")

        else:
            period.append(f"{hour}-{hour+1}")

    df['period'] = period

    return df