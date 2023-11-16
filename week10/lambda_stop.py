import boto3


iam = boto3.client('iam')
lambda_client = boto3.client('lambda')

def Create_Lambda(function_name):
    
    role_response = iam.get_role(RoleName='LabRole')
    handler = open('lambda_stop_function.zip','rb')
    zipped_code = handler.read()

    response = lambda_client.create_function(
        FunctionName = function_name,
        Role = role_response['Role']['Arn'],
        Publish = True,
        PackageType = 'Zip',
        Runtime = 'python3.9',
        Code={
            'ZipFile': zipped_code
        },
        Handler='lambda_stop_function.lambda_handler'
    )

    lambda_client = boto3.client('lambda')

def Invoke_Lambda(function_name):
    invoke_response = lambda_client.invoke(FunctionName = function_name)
    return invoke_response

def main():
    functionName = 'stopEC2'
    try:
        function = lambda_client.get_function(FunctionName=functionName)
        print("Function Already Exists")
    except:
        print("Creating Function")
        response = Create_Lambda(functionName)
    print("Invoking Lambda Function")
    Invoke_Lambda(functionName)

if __name__ == "__main__":
    main()
