import boto3
import StringIO
import zipfile
import mimetypes

s3 = boto3.resource('s3')
portfolio_bucket = s3.Bucket('portfolio.karlekar.com')
build_bucket = s3.Bucket('portfoliobuild.karlekar.com')
sns = boto3.resource('sns')
topic = sns.Topic('arn:aws:sns:us-east-1:219104658389:deployPortfolioTopic')

def lambda_handler(event, context):
    try:
        portfolio_buffer = StringIO.StringIO()
        build_bucket.download_fileobj('portfoliobuild.zip', portfolio_buffer)

        with zipfile.ZipFile(portfolio_buffer) as myzip:
            for nm in myzip.namelist():
                obj = myzip.open(nm)
                portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
                portfolio_bucket.Object(nm).Acl().put(ACL='public-read')
        print "Code pushed!"
        topic.publish(Subject="Portfolio code pushed successfully!", Message="Portfolio code pushed from portfoliobuild.karlekar.com to portfolio.karlekar.com")
    except:
        topic.publish(Subject="Portfolio code push failed!", Message="Portfolio code push from portfoliobuild.karlekar.com to portfolio.karlekar.com failed. Please review the logs.")
    return 'Portfolio Lambda Completed'
