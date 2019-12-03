import boto3
import json
# s3_ops is used to perform S3 based operations
from s3_ops import get_objects


def main():
    # Create the textract client using boto3
    client = boto3.client('textract', region_name='us-east-2')

    # File used to persist textual state which has been extracted
    text_data_file = open("Textual_Data.txt", "a")

    # Counter for how many S3 objects have been analyzed
    object_iter_counter = 0

    # Limit number of objects which are analyzed
    object_limiter = 1

    # S3 Bucket name with contents relevant to the textraction
    bucket_name = "kentextract"

    # Retrieve all of the objects within the given bucket
    all_bucket_objects = get_objects(bucket_name)
    # List used to store all of the words which have been retrieved from documents
    word_list = []
    # For each object in the bucket...
    for obj in all_bucket_objects[0]:
        # Used to limit how many objects to Textract, controlling costs while testing
        if object_iter_counter < object_limiter:
            # Sets the current object to perform work on, specifying the bucket name + file name (via 'key')
            curr_s3_obj = {"Bucket": bucket_name, "Name": obj.key}
            # Build the detection response client with the current object being analyzed
            detect_response = client.detect_document_text(Document={'S3Object': curr_s3_obj})
            # Counter for determining how many objects have been analyzed
            object_iter_counter += 1
            # For each "block" in the detection response...
            for blocks in detect_response['Blocks']:
                # ... Determine if the block is of "WORD"...
                if blocks['BlockType'] == 'WORD':
                    # ... Print the text value(s) for that block
                    print("{}\t".format(blocks['Text']))
                    word_list.append(blocks["Text"])
                    # Write text to text data file
                    text_data_file.write("{}\n".format(blocks['Text']))
            # Printed confirmation re: how many objects/files have been analyzed by Textract
            print("Objects completed thus far:", object_iter_counter)
            json_object = json.dumps(word_list)
            print(blocks["Text"], blocks["Id"])
            print(json_object)

        else:
            pass

    print(len(word_list))
    text_data_file.close()


if __name__ == "__main__":
    main()
