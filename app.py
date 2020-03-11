import os
import random
import shutil 
from modules import facecompare
from modules import pdf2img
from modules import rotimg
from modules import aws
from modules import imgcmprs
from modules import eyeblink
from modules import videoframe
from modules import videoinfo
from modules import videoresize
from modules import fmidtrans
from modules import videocheck
from flask import send_from_directory
from werkzeug.utils import secure_filename
from flask import Flask, request, jsonify, make_response, render_template, send_file, redirect


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


""" Global Variables Declaration """
aws_matched = 95.0
aws_not_matched = 63.0
opencv_matched = 95
rand_min = 10000
rand_max = 99999

ear = 0.2
ear_frame_freq = 4
extract_frame_no = 4
transition_id_strings = 18


#Face Compare API
@app.route("/face_compare_api", methods=['POST'])
def compare():

	""" Accepting the request json which is requested from userside """
	base_pwd = request.form['base_file_password']
	compare_pwd = request.form['compare_file_password']
	finmomenta_trans_id = request.form['finmomenta_transaction_id']
	# request_type = request.form['request_structure_type']

	""" Generate a transaction ID for each API hits """
	trans_id = fmidtrans.transition_id_generator(transition_id_strings)

	""" Partial Response type structure globaly declaration """
	result1 = {}
	result1['code'] = 4001
	result1['status'] = 'Success'
	result1['description'] = 'Matched'
	result1['client_transaction_id'] = trans_id
	result1['finmomenta_transaction_id'] = finmomenta_trans_id

	result2 = {}
	result2['code'] = 4002
	result2['status'] = 'Success'
	result2['description'] = 'Manual Check'
	result2['client_transaction_id'] = trans_id
	result2['finmomenta_transaction_id'] = finmomenta_trans_id

	result3 = {}
	result3['code'] = 4003
	result3['status'] = 'Success'
	result3['description'] = 'Not Matched'
	result3['client_transaction_id'] = trans_id
	result3['finmomenta_transaction_id'] = finmomenta_trans_id

	""" Fully Response Structure type"""

	result4 = {}
	result4['code'] = 4011
	result4['status'] = 'Success'
	result4['description'] = 'Matched'
	result4['client_transaction_id'] = trans_id
	result4['finmomenta_transaction_id'] = finmomenta_trans_id
	result4['file_response'] = ''

	result5 = {}
	result5['code'] = 4012
	result5['status'] = 'Success'
	result5['description'] = 'Matched'
	result5['client_transaction_id'] = trans_id
	result5['finmomenta_transaction_id'] = finmomenta_trans_id
	result5['file_response'] = ''

	result6 = {}
	result6['code'] = 4013
	result6['status'] = 'Success'
	result6['description'] = 'Manual Check'
	result6['client_transaction_id'] = trans_id
	result6['finmomenta_transaction_id'] = finmomenta_trans_id
	result6['file_response'] = ''

	result7 = {}
	result7['code'] = 4014
	result7['status'] = 'Success'
	result7['description'] = 'Manual Check'
	result7['client_transaction_id'] = trans_id
	result7['finmomenta_transaction_id'] = finmomenta_trans_id
	result7['file_response'] = ''

	result8 = {}
	result8['code'] = 4015
	result8['status'] = 'Success'
	result8['description'] = 'Not Matched'
	result8['client_transaction_id'] = trans_id
	result8['finmomenta_transaction_id'] = finmomenta_trans_id
	result8['file_response'] = ''

	# result9 = {}
	# result9['code'] = 4016
	# result9['status'] = 'Success'
	# result9['description'] = 'Not Matched'
	# result9['client_transaction_id'] = trans_id
	# result9['finmomenta_transaction_id'] = finmomenta_trans_id
	# result9['file_response'] = ''

	result10 = {}
	result10['code'] = 4021
	result10['status'] = 'failure'
	result10['description'] = 'Not able to proceed due to poor image quality'
	result10['client_transaction_id'] = trans_id
	result10['finmomenta_transaction_id'] = finmomenta_trans_id

	result11 = {}
	result11['code'] = 4022
	result11['status'] = 'failure'
	result11['description'] = 'Invalid Request, Please upload both images'
	result11['client_transaction_id'] = trans_id
	result11['finmomenta_transaction_id'] = finmomenta_trans_id

	result12 = {}
	result12['code'] = 4023
	result12['status'] = 'failure'
	result12['description'] = 'Base_image pdf is protected by password. Kindly mention correct protect password.'
	result12['client_transaction_id'] = trans_id
	result12['finmomenta_transaction_id'] = finmomenta_trans_id

	result13 = {}
	result13['code'] = 4024
	result13['status'] = 'failure'
	result13['description'] = 'Compare_image pdf is protected by password. Kindly mention correct protect password.'
	result13['client_transaction_id'] = trans_id
	result13['finmomenta_transaction_id'] = finmomenta_trans_id


	""" declaring some global list variables """
	path = []
	numofimage=[]
	uploadedimages = []
	original_image_path = []
	
	""" Creating 'Upload' folder as temporary directory """
	target = os.path.join(APP_ROOT, "upload")
	if not os.path.isdir(target):
			os.mkdir(target)
	else:
		pass

	""" Saving base_image with adding a random number ahead of filename in upload folder """
	for file1 in request.files.getlist('base_file'):
		if len(file1.filename) != 0:
			filename = str(random.randrange(rand_min, rand_max)) + "_" + file1.filename
			destination = "/".join([target, filename])
			file1.save(destination)

			""" if input files is .pdf then converting it into .jpg """
			file_name, file_extension = os.path.splitext(filename)
			if (file_extension == ".pdf"):
				pdf_file = pdf2img.pdf_password_decoder("upload/"+ filename, 'pdf', base_pwd)
				if pdf_file == 0:
					os.remove("upload/"+ filename)
					return jsonify(result12)
				elif pdf_file == 1:
					image = pdf2img.pdf2img("upload/"+filename)
					path.append(image)
					original_image_path.append(image)
					os.remove("upload/"+ filename)	
				else:
					image = pdf2img.pdf2img("upload/"+file_name+"_page_1.pdf")
					os.remove("upload/"+file_name+"_page_1.pdf")
					os.remove("upload/"+file_name+"_page_2.pdf")
					path.append(image)
					original_image_path.append(image)
					os.remove("upload/"+ filename)
			else:
				path.append(filename)
				original_image_path.append(filename)

	""" Saving compare_image with adding a random number ahead of filename in upload folder """
	for file2 in request.files.getlist('compare_file'):
		if len(file2.filename) != 0:
			filename = str(random.randrange(rand_min, rand_max)) + "_" + file2.filename
			destination = "/".join([target, filename])
			file2.save(destination)

			""" if input file is .pdf then converting it into .jpg """
			file_name, file_extension = os.path.splitext(filename)
			if (file_extension == ".pdf"):
				pdf_file = pdf2img.pdf_password_decoder("upload/"+ filename, 'pdf', compare_pwd)
				if pdf_file == 0:
					os.remove("upload/"+ filename)
					return jsonify(result13)
				elif pdf_file == 1:
					image = pdf2img.pdf2img("upload/"+filename)
					path.append(image)
					original_image_path.append(image)
					os.remove("upload/"+ filename)	
				else:
					image = pdf2img.pdf2img("upload/"+file_name+"_page_1.pdf")
					os.remove("upload/"+file_name+"_page_1.pdf")
					os.remove("upload/"+file_name+"_page_2.pdf")
					path.append(image)
					original_image_path.append(image)
					os.remove("upload/"+ filename)
			else:
				path.append(filename)
				original_image_path.append(filename)

	uploadedimages.extend(["upload/"+ x for x in path])

	""" check the input parameters should not more than two parameters """
	if len(path) != 2:
		remove_images(uploadedimages)
		return jsonify(result11)

	""" check our solution is able to detect face in the image or not (for base_image) """
	count  = facecompare.checkImage("upload/"+ path[0])
	if(count == 0):
		newpaths = rotimg.rotation("upload/"+ path[0])
		uploadedimages.extend(newpaths)
		count1 = facecompare.checkImage(newpaths[0])
		count2 = facecompare.checkImage(newpaths[1])
		if(count1 >= count2):
			path[0] = newpaths[0]
			numofimage.append(count1)
		else:
			path[0] = newpaths[1]
			numofimage.append(count2)
	else:
		numofimage.append(count)
		
	""" check our solution is able to detect face in the image or not (for compare_image) """
	count  = facecompare.checkImage("upload/"+ path[1])
	if(count == 0):
		newpaths = rotimg.rotation("upload/"+ path[1])
		uploadedimages.extend(newpaths)
		count1 = facecompare.checkImage(newpaths[0])
		count2 = facecompare.checkImage(newpaths[1])
		if(count1 >= count2):
			path[1] = newpaths[0]
			numofimage.append(count1)
		else:
			path[1] = newpaths[1]
			numofimage.append(count2)
	else:
		numofimage.append(count)


	""" if face is detectable than send it for matching in opencv solution """
	box = {}
	box = facecompare.Input_Image(path[0], path[1], numofimage)


	""" If Our solution (OpenCV) is not able to proceed on image face for partial response """
	if box["numFaces1"] == 0 or box["numFaces2"] == 0 or box["Similarity"][0] == 0:
		try:
			""" check size of the image if it's more than 5mb then compress their size """
			if os.path.getsize("upload/"+ original_image_path[0]) > 5242800:
				imgcmprs.compress("upload/"+ original_image_path[0])
			if os.path.getsize("upload/"+ original_image_path[1]) > 5242800:	
				imgcmprs.compress("upload/"+ original_image_path[1])

			""" Call the AWS API with base_image and compare_image """
			awsbox = aws.AWS_Compare("upload/"+ original_image_path[0], "upload/"+ original_image_path[1])
			remove_images(uploadedimages)

			""" Response conditions if AWS matching confidence is more than 95 or 
			between 63 to 95 or less than 63 """
			if awsbox["Similarity"][0] >= aws_matched:
				return jsonify(result1)

			elif aws_not_matched <= awsbox["Similarity"][0] < aws_matched:
				return jsonify(result2)

			elif awsbox["Similarity"][0] < aws_not_matched:
				return jsonify(result3)
		except:
			remove_images(uploadedimages)
			return jsonify(result10)

	# """ If our solution (OpenCV) gives more than 95 matching confidence """
	elif box["Similarity"][0] >= opencv_matched:
		remove_images(uploadedimages)			
		return jsonify(result1)


	# """ If our solution gives less than 95 matching confidence """
	elif 0 < box["Similarity"][0] < opencv_matched:
		try:
			""" check the size of image if its more than 5MB then compress it """
			if os.path.getsize("upload/"+ original_image_path[0]) > 5242800:
				imgcmprs.compress("upload/"+ original_image_path[0])
			if os.path.getsize("upload/"+ original_image_path[1]) > 5242800:
				imgcmprs.compress("upload/"+ original_image_path[1])	

			""" Call to AWS API with base_image and compare_image """
			awsbox = aws.AWS_Compare("upload/"+ original_image_path[0], "upload/"+ original_image_path[1])
			remove_images(uploadedimages)

			""" Response conditions if AWS matching confidence is more than 95 or
			between 63 to 95 or less than 63 """
			if awsbox["Similarity"][0] >= aws_matched:
				return jsonify(result1)

			elif aws_not_matched <= awsbox["Similarity"][0] < aws_matched:
				return jsonify(result2)

			elif awsbox["Similarity"][0] < aws_not_matched:
				return jsonify(result3)
		except:
			remove_images(uploadedimages)
			return jsonify(result2)


''' For fully response code write condition here

	# If Our solution (OpenCV) is not able to proceed on image face for fully response
	if box["numFaces1"] == 0 or box["numFaces2"] == 0 or box["Similarity"][0] == 0:
		try:
			# check size of the image if it's more than 5mb then compress their size
			if os.path.getsize("upload/"+ original_image_path[0]) > 5242800:
				imgcmprs.compress("upload/"+ original_image_path[0])
			if os.path.getsize("upload/"+ original_image_path[1]) > 5242800:	
				imgcmprs.compress("upload/"+ original_image_path[1])

			# Call the AWS API with base_image and compare_image
			awsbox = aws.AWS_Compare("upload/"+ original_image_path[0], "upload/"+ original_image_path[1])
			remove_images(uploadedimages)

			# Response conditions if AWS matching confidence is more than 95 or between 63 to 95 or less than 63
			if awsbox["Similarity"][0] >= aws_matched:
				result5['file_response'].append(awsbox["json"])
				return jsonify(result5)
				#return jsonify({'Code' : 4001, 'Status': 'Matched', 'Description': awsbox["json"]})

			elif aws_not_matched <= awsbox["Similarity"][0] < aws_matched:
				result7['file_response'].append(awsbox["json"])
				return jsonify(result7)
				#return jsonify({'Code' : 4002, 'Status': 'Manual Check', 'Description': awsbox["json"]})

			elif awsbox["Similarity"][0] < aws_not_matched:
				result8['file_response'].append(awsbox["json"])
				return jsonify(result8)
				#return jsonify({'Code' : 4003, 'Status': 'Fail', 'Description': awsbox["json"]})
		except:
			remove_images(uploadedimages)
			return jsonify(result10)
			#return jsonify({'Code' : 4004, 'Status': 'Fail', 'Description' : 'Not able to proceed due to poor image quality.'})


	# If our solution (OpenCV) gives more than 95 matching confidence
	elif box["Similarity"][0] >= opencv_matched:
		remove_images(uploadedimages)	
		result4['file_response'].append(box["Result"])
		return jsonify(result4)		
		#return jsonify({'Code' : 4000, 'Status': 'Matched', 'Description' : box["Result"]})


	# If our solution gives less than 95 matching confidence
	elif 0 < box["Similarity"][0] < opencv_matched:
		try:
			# check the size of image if its more than 5MB then compress it
			if os.path.getsize("upload/"+ original_image_path[0]) > 5242800:
				imgcmprs.compress("upload/"+ original_image_path[0])
			if os.path.getsize("upload/"+ original_image_path[1]) > 5242800:
				imgcmprs.compress("upload/"+ original_image_path[1])	

			# Call to AWS API with base_image and compare_image
			awsbox = aws.AWS_Compare("upload/"+ original_image_path[0], "upload/"+ original_image_path[1])
			remove_images(uploadedimages)

			# Response conditions if AWS matching confidence is more than 95 or between 63 to 95 or less than 63
			if awsbox["Similarity"][0] >= aws_matched:
				result5['file_response'].append(awsbox["json"])
				return jsonify(result5)
				#return jsonify({'Code' : 4001, 'Status': 'Matched', 'Description': awsbox["json"]})

			elif aws_not_matched <= awsbox["Similarity"][0] < aws_matched:
				result7['file_response'].append(awsbox["json"])
				return jsonify(result7)
				return jsonify({'Code' : 4002, 'Status': 'Manual Check', 'Description': awsbox["json"]})

			elif awsbox["Similarity"][0] < aws_not_matched:
				result8['file_response'].append(awsbox["json"])
				return jsonify(result8)
				#return jsonify({'Code' : 4005, 'Status': 'Not Matched', 'Description' : awsbox["json"]})
		except:
			remove_images(uploadedimages)
			result6['file_response'].append(box["Result"])
			return jsonify(result6)
			#return jsonify({'Code' : 4006, 'Status': 'Manual Check', 'Description': box["Result"]})

End '''


def remove_images(list_of_images):
	""" A common function for deleting all the proceed 
	images from upload/temporary folder """
	try:
		for image in list_of_images:
			os.remove(image)
	except:
		pass




# Liveness-check API
@app.route('/liveness_check_api', methods=['POST']) 
def liveness():

	""" Recieve the video file and save it in upload folder with random number unique identity """
	fm_transition_id = request.form['finmomenta_transaction_id']
	# vendor_id = request.form['vendor_id']

	""" transaction id generator for API hits """
	trans_id = fmidtrans.transition_id_generator(transition_id_strings)


	""" Response Structure globaly declaration """
	result1 = {}
	result1['code'] = 4000
	result1['status'] = 'Success'
	result1['description']  = 'Your liveness check is successful'
	result1['client_transaction_id'] = trans_id
	result1['finmomenta_transaction_id'] = fm_transition_id

	result2 = {}
	result2['code'] = 4011
	result2['status'] = 'failure'
	result2['description']  = 'Liveness check is failed, try again with more than 2 eye blinks.'
	result2['client_transaction_id'] = trans_id
	result2['finmomenta_transaction_id'] = fm_transition_id

	result3 = {}
	result3['code'] = 4012
	result3['status'] = 'failure'
	result3['description']  = 'Unable to proceed either due to no eye blinks or due to poor video quality. Try again.'
	result3['client_transaction_id'] = trans_id
	result3['finmomenta_transaction_id'] = fm_transition_id

	result4 = {}
	result4['code'] = 4013
	result4['status'] = 'failure'
	result4['description']  = 'More than 20-second video is not acceptable'
	result4['client_transaction_id'] = trans_id
	result4['finmomenta_transaction_id'] = fm_transition_id

	result5 = {}
	result5['code'] = 4014
	result5['status'] = 'failure'
	result5['description']  = 'Invalid Request. Please upload one video file'
	result5['client_transaction_id'] = trans_id
	result5['finmomenta_transaction_id'] = fm_transition_id

	result6 = {}
	result6['code'] = 4015
	result6['status'] = 'failure'
	result6['description']  = 'Invalid file format. Only .avi and .mp4 formats are allowed'
	result6['client_transaction_id'] = trans_id
	result6['finmomenta_transaction_id'] = fm_transition_id	


	""" Save the input video into 'upload' folder """
	target = os.path.join(APP_ROOT, "upload")
	if not os.path.isdir(target):
			os.mkdir(target)
	else:
		pass

	path = []


	for upload in request.files.getlist("file"):
		if len(upload.filename) != 0:
			filename = str(random.randrange(rand_min, rand_max)) + "_" + upload.filename
			destination = "/".join([target, filename])
			upload.save(destination)

			name, extension = os.path.splitext(filename)
			ext = extension.lower()
			""" Check the video format is '.avi' and '.mp4' or not """
			if ext == ".avi" or ext == ".mp4":
				path.append(filename)
			else:
				os.remove("upload/"+ filename)
				return jsonify(result6)

	""" checking the number of input files"""
	if len(path) != 1:
		os.remove("upload/"+path[0])
		return jsonify(result5)
	else:
		pass

	""" Check the Video length it should be less than 20 sec."""
	vidlen = videoinfo.getDuration("upload/"+path[0])
	if vidlen > 20:
		os.remove("upload/"+path[0])
		return jsonify(result4)
	else:
		pass

	""" Check the video frame per second """
	fps_info = videoinfo.VideoInfo("upload/"+path[0])


	""" if Video is recorded by any Mobile camera(front + back) """
	if fps_info[0] >= 14:
		video = "upload/"+path[0]
		output_path = video[:-4]+'_.mp4'
		try:
			""" call to video_check function for ffmpeg (Rotation of video and fixing the fps=14) """
			vc = videocheck.video_check(video, output_path, '14')

			""" Resizing the video into 512*640 pixels """
			fc = videoresize.video_resize(output_path)

			""" Counting the Eye Blinks via calling eyeblink.py """
			total = eyeblink.eye_blink_count(fc, ear, ear_frame_freq)

			if total >= 2:
				os.remove("upload/"+path[0])
				os.remove(output_path)
				os.remove(fc)
				return jsonify(result1)
			elif total == 1:
				os.remove("upload/"+path[0])
				os.remove(output_path)
				os.remove(fc)
				return jsonify(result2)
			elif total == 0:
				os.remove("upload/"+path[0])
				os.remove(output_path)
				os.remove(fc)
				return jsonify(result3)
			else:
				if path.exists("upload/"+path[0]):
					os.remove("upload/"+path[0])
				if path.exists(output_path):
					os.remove(output_path)
				if path.exists(fc):
					os.remove(fc)
				return jsonify(result3)
		except:
			os.remove("upload/"+path[0])
			return jsonify(result3)

	# """ If video is recorded by any other device like respberrypi or Laptop camera """
	elif fps_info[0] < 14:
		try:
			total = eyeblink.eye_blink_count("upload/"+path[0], ear, ear_frame_freq)

			if total >= 2:
				os.remove("upload/"+path[0])
				return jsonify(result1)
			elif total == 1:
				os.remove("upload/"+path[0])
				return jsonify(result2)
			elif total == 0:
				os.remove("upload/"+path[0])
				return jsonify(result3)
			else:
				if path.exists("upload/"+path[0]):
					os.remove("upload/"+path[0])
				return jsonify(result3)
		except:
			os.remove("upload/"+path[0])
			return jsonify(result3)



#Liveness-frame API
@app.route('/liveness_frame_api', methods=['POST']) 
def livenessframe():
	# print(request.headers)

	""" Accepting input parameters """
	fm_transaction_id = request.form['finmomenta_transaction_id']
	# vendor_id = request.form['vendor_id']

	""" Transaction number generator """
	trans_id = fmidtrans.transition_id_generator(transition_id_strings)

	""" Response Structure globaly declaration """
	result1 = {}
	result1['code'] = 4000
	result1['status'] = 'Success'
	result1['description']  = 'Your liveness check is successful'
	result1['client_transaction_id'] = trans_id
	result1['finmomenta_transaction_id'] = fm_transaction_id
	result1['file_response'] = []

	result2 = {}
	result2['code'] = 4011
	result2['status'] = 'failure'
	result2['description']  = 'Liveness check is failed, try again with more than 2 eye blinks.'
	result2['client_transaction_id'] = trans_id
	result2['finmomenta_transaction_id'] = fm_transaction_id

	result3 = {}
	result3['code'] = 4012
	result3['status'] = 'failure'
	result3['description']  = 'Unable to proceed either due to no eye blinks or due to poor video quality. Try again.'
	result3['client_transaction_id'] = trans_id
	result3['finmomenta_transaction_id'] = fm_transaction_id

	result4 = {}
	result4['code'] = 4013
	result4['status'] = 'failure'
	result4['description']  = 'More than 20-second video is not acceptable'
	result4['client_transaction_id'] = trans_id
	result4['finmomenta_transaction_id'] = fm_transaction_id

	result5 = {}
	result5['code'] = 4014
	result5['status'] = 'failure'
	result5['description']  = 'Invalid Request. Please upload one video file'
	result5['client_transaction_id'] = trans_id
	result5['finmomenta_transaction_id'] = fm_transaction_id

	result6 = {}
	result6['code'] = 4015
	result6['status'] = 'failure'
	result6['description']  = 'Invalid file format. Only .avi and .mp4 formats are allowed'
	result6['client_transaction_id'] = trans_id
	result6['finmomenta_transaction_id'] = fm_transaction_id	

	
	""" Saveing the input video file in 'upload' folder """
	target = os.path.join(APP_ROOT, "upload")
	if not os.path.isdir(target):
			os.mkdir(target)
	else:
		pass

	path = []


	for upload in request.files.getlist("file"):
		if len(upload.filename) != 0:
			filename = str(random.randrange(rand_min, rand_max)) + "_" + upload.filename
			destination = "/".join([target, filename])
			upload.save(destination)

			""" Checking the file formats (It should be '.avi', '.mp4') """
			name, extension = os.path.splitext(filename)
			ext = extension.lower()
			if ext == ".avi" or ext == ".mp4":
				path.append(filename)
			else:
				os.remove("upload/"+ filename)
				return jsonify(result6)


	""" checking for files input requirements """
	if len(path) != 1:
		os.remove("upload/"+path[0])
		return jsonify(result5)
	else:
		pass


	""" checking the length duration of input video file """
	vidlen = videoinfo.getDuration("upload/"+path[0])
	if vidlen > 20:
		os.remove("upload/"+path[0])
		return jsonify(result4)
	else:
		pass

	""" check the frame per second and define that video is capture via mobile phone or laptop """
	fps_info = videoinfo.VideoInfo("upload/"+path[0])


	""" If video is captured by mobile phone mostly having more than 14 fps """
	if fps_info[0] >= 14:
		video = "upload/"+path[0]
		output_path = video[:-4]+'_.mp4'
		try:
			""" Rotating the mobile recorded video file in ffmpeg
			 and fixing fps value is 14 for all inputs. """
			vc = videocheck.video_check(video, output_path, '14')

			""" Resize the video into 512*620 pixels """
			fc = videoresize.video_resize(output_path)

			""" Calling function for counting Eye Blinks in a video """
			total = eyeblink.eye_blink_count(fc, ear, ear_frame_freq)

			""" Sending the same video for extracting a frame and get reponse in base64 code """
			frame = videoframe.extract_image_one_fps(fc, extract_frame_no)
			frameimg = videoframe.encodeimage(frame)
			os.remove(frame)
			result1["file_response"].append(frameimg)

			if total >= 2:
				os.remove("upload/"+path[0])
				os.remove(output_path)
				os.remove(fc)
				return jsonify(result1)
			elif total == 1:
				os.remove("upload/"+path[0])
				os.remove(output_path)
				os.remove(fc)
				return jsonify(result2)
			elif total == 0:
				os.remove("upload/"+path[0])
				os.remove(output_path)
				os.remove(fc)
				return jsonify(result3)
			else:
				if path.exists("upload/"+path[0]):
					os.remove("upload/"+path[0])
				if path.exists(output_path):
					os.remove(output_path)
				if path.exists(fc):
					os.remove(fc)
				return jsonify(result3)
		except:
			os.remove("upload/"+path[0])
			return jsonify(result3)

	# """ Captured video via Laptop or other camera device """
	elif fps_info[0] < 14:
		try:
			total = eyeblink.eye_blink_count("upload/"+path[0], ear, ear_frame_freq)
			frame = videoframe.extract_image_one_fps("upload/"+path[0], extract_frame_no)
			frameimg = videoframe.encodeimage(frame)
			result1["file_response"].append(frameimg)
			os.remove(frame)

			if total >= 2:
				os.remove("upload/"+path[0])
				return jsonify(result1)
			elif total == 1:
				os.remove("upload/"+path[0])
				return jsonify(result2)
			elif total == 0:
				os.remove("upload/"+path[0])
				return jsonify(result3)
			else:
				if path.exists("upload/"+path[0]):
					os.remove("upload/"+path[0])
				return jsonify(result3)
		except:
			os.remove("upload/"+path[0])
			return jsonify(result3)




#Frames Extraction API
@app.route('/frame_extract_api', methods=['POST']) 
def videoframes():

	""" Accepting input parameters from client side """
	fm_transaction_id = request.form['finmomenta_transaction_id']
	# vendor_id = request.form['vendor_id']

	""" Transaction number generator """
	trans_id = fmidtrans.transition_id_generator(transition_id_strings)

	""" Response Structure globaly declaration """
	result1 = {}
	result1['code'] = 4001
	result1['status'] = 'Success'
	result1['description']  = 'One image extracted successfully'
	result1['client_transaction_id'] = trans_id
	result1['finmomenta_transaction_id'] = fm_transaction_id
	result1['file_response'] = []

	result2 = {}
	result2['code'] = 4016
	result2['status'] = 'failure'
	result2['description']  = 'Not able to process, try again'
	result2['client_transaction_id'] = trans_id
	result2['finmomenta_transaction_id'] = fm_transaction_id

	result3 = {}
	result3['code'] = 4017
	result3['status'] = 'failure'
	result3['description']  = 'Invalid Request. Please upload one video file'
	result3['client_transaction_id'] = trans_id
	result3['finmomenta_transaction_id'] = fm_transaction_id

	result4 = {}
	result4['code'] = 4018
	result4['status'] = 'failure'
	result4['description']  = 'Invalid file format. Only .avi and .mp4 formats are allowed'
	result4['client_transaction_id'] = trans_id
	result4['finmomenta_transaction_id'] = fm_transaction_id

	result5 = {}
	result5['code'] = 4019
	result5['status'] = 'failure'
	result5['description']  = 'More than 20-second video is not acceptable.'
	result5['client_transaction_id'] = trans_id
	result5['finmomenta_transaction_id'] = fm_transaction_id

	""" Creating 'upload' folder as temporary process """
	target = os.path.join(APP_ROOT, "upload")
	if not os.path.isdir(target):
			os.mkdir(target)
	else:
		pass

	path = []

	""" Accepting input file and add a random number ahead of 
	filename and save it in upload folder """

	for upload in request.files.getlist("file"):
		if len(upload.filename) != 0:
			filename = str(random.randrange(rand_min, rand_max)) + "_" + upload.filename
			destination = "/".join([target, filename])
			upload.save(destination)

			""" Check the file formats """
			name, extension = os.path.splitext(filename)
			ext = extension.lower()
			if ext == ".avi" or ext == ".mp4":
				path.append(filename)
			else:
				os.remove("upload/"+ filename)
				return jsonify(result4)

	""" checking the input parameters """
	if len(path) != 1:
		os.remove("upload/"+path[0])
		return jsonify(result3)
	else:
		pass

	""" Checking the video length (duration) """
	vidlen = videoinfo.getDuration("upload/"+path[0])
	if vidlen > 20:
		os.remove("upload/"+path[0])
		return jsonify(result5)
	else:
		pass

	# fps_info = videoinfo.VideoInfo("upload/"+path[0])
	video = "upload/"+path[0]
	output_path = video[:-4]+'_.mp4'

	try:
		""" Rotating Video and fixing ( fps = 14 ) """
		vc = videocheck.video_check(video, output_path, '14')

		""" Resizing Video in desired pixel """
		fc = videoresize.video_resize(output_path)

		""" Requesting for a single frame from a video """
		frame = videoframe.extract_image_one_fps(fc, extract_frame_no)

		""" Converting frame image into base64 code """
		frameimg = videoframe.encodeimage(frame)
		result1['file_response'].append(frameimg)

		""" deleting all the proceed file from temporary folder """
		os.remove(frame)
		os.remove(video)
		os.remove(fc)
		os.remove(output_path)
		# response = send_file(frames, mimetype = "image/png")
		return jsonify(result1)

	except:
		os.remove("upload/"+path[0])
		return jsonify(result2)



@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4555, debug=True)

