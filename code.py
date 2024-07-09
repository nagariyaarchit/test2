import sys
from csv import DictReader
import csv
import json
import boto3, sys
import requests
from datetime import date
import os

endpoint = os.environ['GraphEndPoint']
url = os.environ['Auth0Endpoint']
processd_bucket = os.environ['ProcessedBucket']

if not (endpoint):
    endpoint = 'https://dx-gateway.dev.aws.wfscorp.com/graphql'

client_id = os.environ['client_id']
sns_topic_arn = os.environ['AlarmNotificationTopic']
client_secret_parameter_name = os.environ['client_secret_parameter_name']
jsm_project_id = os.environ['JSMProjectID']
s3_client = boto3.client('s3')
s3 = boto3.resource('s3')

ssm_client = boto3.client('ssm', region_name=os.environ['AWS_REGION'])
sns = boto3.client("sns")
failure_array = []


def _call_auth_service():
    client_secret_ssm_parameter = ssm_client.get_parameter(Name=client_secret_parameter_name, WithDecryption=True)
    client_secret = client_secret_ssm_parameter['Parameter']['Value']

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": "https://dx-graph.wfscorp.com",
        "grant_type": "client_credentials"

    }
    response = requests.post(
        url,
        data=data
    )
    response = response.json()

    return (response['access_token'])


def _send_message(error_filename, data_array):
    if (len(data_array) > 0):

        msg = "Following records were not processed in " + error_filename + ":\n"
        emailable_keys = ['Employee_ID', 'Effective_Date', 'Transaction_Type', 'Transaction_Status', 'New Field']

        for record in data_array:
            emailable_record = {key: record[key] for key in emailable_keys if key in record}
            emailable_record_str = str(emailable_record)
            msg = msg + emailable_record_str + "\n"

        response = sns.publish(
            TopicArn=sns_topic_arn,
            Message=msg,
            Subject="Failure to process Employee records from workday worker lambda"
        )


def _move_files(filekey, bucket):
    copy_source = {
        'Bucket': bucket,
        'Key': filekey
    }
    # bucket = s3.Bucket(bucket)
    key = filekey.split("/")
    # bucket.copy(copy_source, '/processed/{}'.format(key[1]))
    my_date = date.today()  # Get today's date
    s3_client.copy_object(Bucket=processd_bucket, CopySource=copy_source, Key='processed/{}'.format(filekey))
    s3_client.delete_object(Bucket=bucket, Key=filekey)


def _sanitize_parameter(input_parameter):
    special_character_mapping = {
        'à': 'a',
        'á': 'a',
        'â': 'a',
        'ã': 'a',
        'ä': 'a',
        'å': 'a',
        'è': 'e',
        'é': 'e',
        'ê': 'e',
        'ë': 'e',
        'É': 'E',
        'ì': 'i',
        'í': 'i',
        'î': 'i',
        'ï': 'i',
        'ò': 'o',
        'ó': 'o',
        'ô': 'o',
        'õ': 'o',
        'ö': 'o',
        'ù': 'u',
        'ú': 'u',
        'û': 'u',
        'ü': 'u',
    }

    sanitized_string = ''.join(special_character_mapping.get(char, char) for char in input_parameter)

    return sanitized_string


def _send_message(access_token, employee_info, label):
    ticket_type = label
    if label == 'ManagerUpdate':
        label = "UpdateEmployee"

    query = """
        mutation Mutation($input: ServiceRequestInputType!) {
        createJiraServiceRequest(input: $input)
        }
        """
    headers = {
        "Authorization": 'Bearer {}'.format(access_token),
        "x-wfs-client-name": 'postman',
        "x-wfs-client-version": '1.0.0',
    }
    employee = {
        "description": employee_info,
        "labels": ticket_type,
        "projectId": jsm_project_id,
        "type": label
    }
    variables = {'input': employee}
    print({"query": query, "variables": variables})
    response = requests.post(endpoint,
                             json={"query": query, "variables": variables},
                             headers=headers
                             )
    response = response.json()
    print(response)
    status = response.get('data', {}).get('createJiraServiceRequest', {}).get('status')

    return status


def _create_jsm_tickets(access_token, employeedata =None, label=None):
    employee_info = {}
    for empdata in employeedata:
        old_emp = empdata
        empdata = empdata.replace(" ", "_")
        empdata = empdata.replace(":", "")
        employee_info[empdata] = employeedata[old_emp]
        employee_info[empdata] = employee_info[empdata].strip()
    # change date to yyyy-mm-dd
    data = employee_info['Effective_Date']
    employee_info['First_Name'] = _sanitize_parameter(employee_info.get('First_Name'))
    employee_info['Middle_Name'] = _sanitize_parameter(employee_info.get('Middle_Name'))
    employee_info['Last_Name'] = _sanitize_parameter(employee_info.get('Last_Name'))
    data = data.split("/")
    new_date = "{}-{}-{}".format(data[2], data[0], data[1])
    employee_info['Effective_Date'] = new_date
    if employee_info['Time_Zone'] == "GMT United Kingdom Time (London)":
        employee_info['Time_Zone'] = "GMT+00:00 United Kingdom Time (London)"
    if 'Device' in employee_info:
        if "Mac Advanced Computer System (Advanced Devices" in employee_info['Device']:
            employee_info[
                'Device'] = "Mac Advanced Computer System (Advanced devices are typically used in IT roles such as " \
                            "Developers, Architects, Engineers, and QA Automation)"
        elif "Windows Advanced Computer System (Advanced Devices Are" in employee_info['Device']:
            employee_info[
                'Device'] = "Windows Advanced Computer System (Advanced devices are typically used in IT roles such " \
                            "as Developers, Architects, Engineers, and QA Automation)"
        if not employee_info['Device']:
            employee_info['Device'] = "No Equipment Required"
        if not employee_info['Monitor']:
            employee_info['Monitor'] = "No Monitor"
    try:
        status = _send_message(access_token, employee_info, label)
        if status != 201:
            print("Ticket fail to create")
            failure_array.append(employee_info)
    except:
        failure_array.append(employee_info)


def process_manager_update_file(auth_access_token, file_path):
    manager_data = {}
    with open(file_path, encoding='utf-8-sig') as csvf:
        csv_reader = csv.DictReader(csvf)
        for rows in csv_reader:
            if len(manager_data) == 2000:
                status = _send_message(auth_access_token, manager_data, "ManagerUpdate")
                print(status)
                manager_data = {}
            manager_data[rows['Employee_ID']] = rows['Manager_ID']
        if len(manager_data) > 0:
            print("creating a new ticket")
            status = _send_message(auth_access_token, manager_data, "ManagerUpdate")
            print(status)
    return {
        'status': 200,
        'message': 'processed the file'
    }

def handler(event, context):
    data = event['Records'][0]
    bucket_name = data['s3']['bucket']['name']
    bucket_key = data['s3']['object']['key']
    print(data)
    filename = bucket_key
    label = ""
    print("Authenicating and retrieving Auth0 access token")
    try:
        auth_access_token = _call_auth_service()
    except:
        error_msg = "Unable to retrieve Access token from Auth0 resulting in a unprocessed workday file: " + filename
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=error_msg,
            Subject="Failure to process Employee records from workday worker lambda"
        )
        raise Exception("Unable to retrieve Access token from Auth0")

    print("Downloading the file")
    s3_client.download_file(bucket_name, bucket_key, '/tmp/{}'.format(filename))
    if bucket_key.startswith('WD_Manager_Update'):
        print("calling update manager methods")
        status = process_manager_update_file(auth_access_token, '/tmp/{}'.format(filename))
        _move_files(bucket_key, bucket_name)
        return status

    sucessfully_complete = ["Successfully Completed", "Corrected"]
    sucessfully_rescinded = ["Rescinded"]
    termination_flag = ["Terminate Employee", "End Contingent Worker Contract"]
    hire_employee = ["Hire Employee", "Contract Contingent Worker"]
    update_employee = ["Change Business Title", "Change Job", "Move Worker Staffing", "Request Leave of Absence",
                       "Request Return from Leave of Absence", "Change Legal Name", "Change Preferred Name",
                       "Inactivate Organization Assign Worker Move Workers Divide Organization",
                       "Promote Employee Inbound Promote Employee", "Change Organization Assignments for Worker",
                       "Transfer Employee Inbound Transfer Employee",
                       "Inactivate Organization Assign Worker Move Workers Divide Organization"]

    with open('/tmp/{}'.format(filename), 'r') as f:
        dict_reader = DictReader(f)
        list_of_dicts = list(dict_reader)
        for list_of_dict in list_of_dicts:
            list_of_temp_dict = {}
            for k, v in list_of_dict.items():
                print(k, v)
                list_of_temp_dict[k.lstrip()] = v
            print(list_of_temp_dict['Transaction Type'], list_of_temp_dict['Transaction Status'])
            print("=================================================")
            transaction_type = list_of_temp_dict['Transaction Type']
            if transaction_type in termination_flag:
                if list_of_temp_dict['Transaction Status'] in sucessfully_rescinded:
                    label = "TerminateRescind"
                elif list_of_temp_dict['Transaction Status'] == 'Corrected':
                    label = "TermCorrection"
                elif list_of_temp_dict['Transaction Status'] in sucessfully_complete:
                    if list_of_temp_dict['Comments'] == 'TERM NOW':
                        label = "TerminateNow"
                    else:
                        label = "TerminateEmployee"
            elif transaction_type in hire_employee:
                if list_of_temp_dict['Transaction Status'] in sucessfully_complete:
                    if 'New Field' in list_of_temp_dict:
                        if list_of_temp_dict['New Field'] == 'Hire_Employee_Hire_Employee_Rehire':
                            label = "RehireEmployee"
                        elif list_of_temp_dict['New Field'] == 'CONVERSION':
                            label = "ConvertEmployee"
                        else:
                            label = "OnboardEmployee"
                    else:
                        label = "OnboardEmployee"
                elif list_of_temp_dict['Transaction Status'] in sucessfully_rescinded:
                    label = "NewHireRescind"

            elif transaction_type in update_employee:
                if list_of_temp_dict['Transaction Status'] in sucessfully_complete:
                    label = "UpdateEmployee"
            else:
                return {
                    "message": "unknown option"
                }
            print(label)
            _create_jsm_tickets(auth_access_token, list_of_temp_dict, label)
    _send_message(filename, failure_array)
    _move_files(bucket_key, bucket_name)