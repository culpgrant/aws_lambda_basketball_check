import json
import requests
import boto3

# URL to request basketball data from
url = 'https://public.leagueapps.io/v1/sites/10301/programs/current?x-api-key=663b39a417956b5be106911d4c217738&_=1619649153326&callback=axiosJsonpCallback2'

def get_data_func():
  """
  A function to return the data from the URL above that met the filter criteria I specified.
  """
    response = requests.get(url)
    text_response = response.text
    base_data = json.loads(text_response[20:-3])
    base_basketball_data = [item for item in base_data if item['sport'] == 'Basketball' and item['deleted'] == False]
    # It occurs on a weekend
    filtered_data = [item for item in base_basketball_data if item['scheduleDays'] == 'Sun' or item['scheduleDays'] == 'Sat']
    # Timestamp is April 28th 2021
    filtered_data = [item for item in filtered_data if item['startTime'] > 1619651770000]
    data_send = []
    for row in filtered_data:
        element = {'programId': row['programId'], 'name': row['name'], 'startTime': row['startTime'],
              'gender': row['gender'], 'location': row['location'], 'level': row['experienceLevel'],
              'days': row['scheduleDays'], 'times': row['scheduleTimes'], 'url': row['programUrlHtml'][2:]}
        data_send.append(element)
    num_leages_found = len(data_send)
    return num_leages_found, data_send

num_leages, data_found = get_data_func()

def send_email_func():
  """
  Function to send the email to me
  """
    SENDER = "Grant Culp <culpgrant21@gmail.com>"
    RECIPIENT = "culpgrant21@gmail.com"
    AWS_REGION = "us-east-2"
    SUBJECT = "Amazon Test Email"
    BODY_TEXT = f"""
    There were {num_leages} league(s) found. \r \n
    Here is the data: {data_found}
    """
    CHARSET = "UTF-8"
    client = boto3.client('ses', region_name=AWS_REGION)
    response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )
    return response

def lambda_handler(event, context):
    # Only send the email if we found at least one matching league
    if num_leages > 0:
        em_response = send_email_func()
    else:
        em_response = "No Email Sent"
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!'),
        'email_response': em_response
    }
