import boto3
import StringIO
import zipfile
import mimetypes

def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    portfolio_bucket = s3.Bucket('portfolio.karlekar.com')
    build_bucket = s3.Bucket('portfoliobuild.karlekar.com')

    portfolio_buffer = StringIO.StringIO()
    build_bucket.download_fileobj('portfoliobuild.zip', portfolio_buffer)

    with zipfile.ZipFile(portfolio_buffer) as myzip:
        for nm in myzip.namelist():
            obj = myzip.open(nm)
            portfolio_bucket.upload_fileobj(obj, nm, ExtraArgs={'ContentType': mimetypes.guess_type(nm)[0]})
            portfolio_bucket.Object(nm).Acl().put(ACL='public-read')

    print "Code pushed!"
    return 'Code Pushed by Lambda'
