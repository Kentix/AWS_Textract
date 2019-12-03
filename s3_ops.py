import boto3

s3 = boto3.resource('s3')


def count_objects(bucketname):  # Function to determine how many object exist in a given bucket
    my_bucket = s3.Bucket(bucketname)
    s3obj_count = 0
    for file in my_bucket.objects.all():
        s3obj_count += 1
    return s3obj_count


def get_objects(bucketname):  # Function to put all objects in a given bucket inside of a list
    my_bucket = s3.Bucket(bucketname)
    s3_obj_list = []

    for file in my_bucket.objects.all():
        s3_obj_list.append(file)

    return [s3_obj_list]

