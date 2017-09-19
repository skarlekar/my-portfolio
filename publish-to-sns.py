import boto3

sns = boto3.resource('sns')
topic = sns.Topic('arn:aws:sns:us-east-1:219104658389:deployPortfolioTopic')
response = topic.publish(Subject="Test from python code", Message="Straight from Python code")
