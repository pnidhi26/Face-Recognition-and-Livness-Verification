import boto3
import base64


# AWS API calling with base_image and compare_image
def AWS_Compare(sourceFile, targetFile):
    client=boto3.client('rekognition')

    imageSource=open(sourceFile,'rb')
    imageTarget=open(targetFile,'rb')


    response=client.compare_faces(SimilarityThreshold=0.0,
                                SourceImage={'Bytes': imageSource.read()},
                                TargetImage={'Bytes': imageTarget.read()})


    awsbox = {}
    awsbox["Similarity"] = [0]
    final = []

    for faceMatch in response['FaceMatches']:
        SimilarityThreshold = faceMatch['Similarity']
        conf = round(SimilarityThreshold,2)
        if awsbox["Similarity"][0] < conf:
            awsbox["Similarity"][0] = conf
            

    box = {
        "Base_image": str(encodeImage(sourceFile)),
        "Compared_with": str(encodeImage(targetFile)),
        "Response": str(response)
    }

    final.append(box)
    awsbox["json"] = final
    return awsbox

# converting images into base64 code
def encodeImage(filename):
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    return(encoded_string.decode("utf-8"))
