# Face-Recognition-and-Livness-Verification
Solutions for "Digital e-KYC Verification" for hassle-free and paperless verification processes using Data Science techniques like Computer Vision and Deep Learning domains on projects for Face Detection and Recognition, Liveness Video Analysis, Face Expressions Detection and Restful APIs.


please install all the requirements packages and then run this API. follow the below statements step by step:

1. activate your virtualenv by below command:
   $ -source venv/bin/activate


2. cd to the directory where requirements.txt is located.


3. run: pip install -r requirements.txt   
		or  
	pip install --user --requirement requirements.txt


4. run: cd app/python app.py


5. http://127.0.0.1:4555 run this url in your favourite browser(Chrome/Postman).


//////////     [ 1. Face Compare API ]     ///////////

Chrome URL(Demo) : http://dev-kyd.tachyloans.com:4555/facecompare
Postman API URL : http://127.0.0.1:4555/face_compare_api

Limitation: 
1. Pdf file should be only of one page.

API Request:
{
    'base_file' : 'example1.jpg',
    'base_file_password' : '',        //  Only for protect password with pdf
    'compare_file' : 'example2.jpg'   // Supported formats .jpeg, .jpg, .png, .pdf
    'compare_file_password' : '',     // Only for protect password with pdf
    'finmomenta_transaction_id' : ""  // Tachyloans Transaction ID
    #'vendor_Id' : ""                  // Partial or fully response ID/Code
} 

*Success Response:  

1. Partial Response for Banks or Non Technical company:
{
    'code' : 4001,
    'status' : 'success'
    'description' : 'Matched'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

{
    'code' : 4002,
    'status' : 'success'
    'description' : 'Manual Check'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

{
    'code' : 4003,
    'status' : 'success'
    'description' : 'Not Matched'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

2. Fully Response for Technical company:

{
    'code' : 4011,
    'status' : 'success'
    'description' : 'Matched'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
    'file_response': '{Base64, OpenCV confidence etc.}'
}

{
    'code' : 4012,
    'status' : 'success'
    'description' : 'Matched'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
    'file_response': '{base64, AWS confidence}'
}

{
    'code' : 4013,
    'status' : 'success'
    'description' : 'Manual Check'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
    'file_response':'{Base64, OpenCV confidence etc.}'
}

{
    'code' : 4014,
    'status' : 'success'
    'description' : 'Manual Check'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
    'file_response':'{base64, AWS confidence}'
}

{
    'code' : 4015,
    'status' : 'success'
    'description' : 'Not Matched'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
     'file_response':'{base64, AWS confidence}'
}

*Failure Response: 

{
    'code' : 4021,
    'status' : 'failure'
    'description' : ''Not able to proceed due to poor image quality.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

{
    'code' : 4022,
    'status' : 'failure'
    'description' : 'Invalid Request, Please upload both images.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

{
    'code' : 4023,
    'status' : 'failure'
    'description' : 'Base_image pdf is protected by password. Kindly mention correct protect password.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

{
    'code' : 4024,
    'status' : 'failure'
    'description' : 'Compare_image pdf is protected by password. Kindly mention correct protect password.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

===============================================

For fully Response:

Result type1: (OpenCV Response)

"Base_image" : base64 code of face
"Compare_image" : base64 code of face
"Similarity" : "Numerical value"

Result type2:  (AWS Response)

"Base_image" : base64 code of image
"Compare_image" : base64 code of image
"Response": "{'SourceImageFace': {'BoundingBox': {'Width': 0.13968129456043243, 'Height': 0.3424930274486542, 'Left': 0.45242851972579956, 'Top': 0.2825939655303955}, 'Confidence': 99.99995422363281}, 'FaceMatches': [{'Similarity': 97.30288696289062, 
'Face': {'BoundingBox': {'Width': 0.09004504978656769, 'Height': 0.08553660660982132, 'Left': 0.20093435049057007, 'Top': 0.5280358195304871}, 'Confidence': 99.99966430664062, 'Landmarks': [{'Type': 'eyeLeft', 'X': 0.23333707451820374, 'Y': 0.5597848892211914},
{'Type': 'eyeRight', 'X': 0.2736143171787262, 'Y': 0.5579498410224915}, {'Type': 'mouthLeft', 'X': 0.23947139084339142, 'Y': 0.5929080843925476}, {'Type': 'mouthRight', 'X': 0.2727835476398468, 'Y': 0.5913439989089966}, {'Type': 'nose', 'X': 0.2591371536254883, 'Y': 0.5761262774467468}],
'Pose': {'Roll': -3.7745304107666016, 'Yaw': 10.588261604309082, 'Pitch': -6.5725998878479}, 'Quality': {'Brightness': 58.51073455810547, 'Sharpness': 20.927310943603516}}}], 'UnmatchedFaces': [], 'ResponseMetadata': {'RequestId': '665aa4d5-a6dd-4477-92bb-ceb1c816a730', 'HTTPStatusCode': 200,
'HTTPHeaders': {'content-type': 'application/x-amz-json-1.1', 'date': 'Tue, 24 Sep 2019 12:45:16 GMT', 'x-amzn-requestid': '665aa4d5-a6dd-4477-92bb-ceb1c816a730', 'content-length': '914', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}"




//////////      [ 2. Liveness Check API ]    //////////

Note:
- First you need to capture 10 sec video with APK. Go with APK URL and download it in your phone and capture video.
- You can run it with 20 sec video in Postman aslo.

Postman URL : http://127.0.0.1:4555/liveness_check_api
APK URL :  https://finmomenta-workspace.slack.com/files/UFLT3SLAE/FNJ1C9YQY/app-debug.apk 


API Request:

{
    'file' : 'video.mp4'                 // Supported formats .avi, .mp4
    'finmomenta_transaction_id' : " "
}


API Response:

*Success Response:

{
    'code' : 4000,
    'status' : 'success'
    'description' : 'Your liveness check is successful.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}


*Failure Response:

{
    'code' : 4011,
    'status' : 'failure'
    'description' : 'Liveness check is failed, try again with more than 2 eye blinks.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

{
    'code' : 4012,
    'status' : 'failure'
    'description' : 'Unable to proceed either due to no eye blinks or due to poor video quality. Try again.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

{
    'code' : 4013,
    'status' : 'failure'
    'description' : 'More than 20-second video is not acceptable'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

{
    'code' : 4014,
    'status' : 'failure'
    'description' : 'Invalid Request. Please upload one video file'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

{
    'code' : 4015,
    'status' : 'failure'
    'description' : 'Invalid file format. Only .avi and .mp4 formats are allowed'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}




/////////     [ 3.  Liveness-Frame Combo API]     ///////////


Postman URL :   http://127.0.0.1:4555/liveness_frame_api


API Request:

{
    'file' : 'video.mp4'                // Supported formats .avi, .mp4
    'finmomenta_transaction_id' : ""
}


API Response:

*Success Response:

{
    'code' : 4000,
    'status' : 'success'
    'description' : 'Your liveness check is successful.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : '',
    'file_response' : 'Base64 code of one frame'  
}
   
   
*Failure Response:

{
    'code' : 4011,
    'status' : 'failure'
    'description' : 'Liveness check is failed, try again with more than 2 eye blinks.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

{
    'code' : 4012,
    'status' : 'failure'
    'description' : 'Unable to proceed either due to no eye blinks or due to poor video quality. Try again.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

{
    'code' : 4013,
    'status' : 'failure'
    'description' : 'More than 20-second video is not acceptable.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : '' 
}

{
    'code' : 4014,
    'status' : 'failure'
    'description' : 'Invalid Request. Please upload one video file'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''  
}

{
    'code' : 4015,
    'status' : 'failure'
    'description' : 'Invalid file format. Only .avi and .mp4 formats are allowed.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''  
}




///////////     [ 4.  Frame Extraction API]     ////////////


Postman URL :   http://127.0.0.1:4555/frame_extract_api

API Request:

{
    'file' : 'video.mp4'               // Supported formats .avi, .mp4
    'finmomenta_transaction_id' : ""
}


Response:

*Success Response:

{
    'code' : 4001,
    'status' : 'success'
    'description' : 'One image extracted successfully.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : '',
    'file_response' : ['base64 code of one frame']  
}
   

*Failure Response:

{
    'code' : 4016,
    'status' : 'failure'
    'description' : 'Not able to process, try again.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

{
    'code' : 4017,
    'status' : 'failure'
    'description' : 'Invalid Request. Please upload one video file.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}

{
    'code' : 4018,
    'status' : 'failure'
    'description' : 'Invalid file format. Only .avi and .mp4 formats are allowed.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''   
}

{
    'code' : 4019,
    'status' : 'failure'
    'description' : 'More than 20-second video is not acceptable.'
    'client_transaction_id' : '',
    'finmomenta_transaction_id' : ''
}
















