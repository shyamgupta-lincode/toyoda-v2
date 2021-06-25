import os
import cv2
import numpy as np
import tensorflow as tf
import sys
from utils import label_map_util
from utils import visualization_utils as vis_util
from common_utils import *
from model_settings import *


def load_detector(model_path, NUM_CLASSES):
	PATH_TO_CKPT = os.path.join(model_path,'frozen_inference_graph.pb')
	PATH_TO_LABELS = os.path.join(model_path,'labelmap.pbtxt')
	label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
	categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
	category_index = label_map_util.create_category_index(categories)

	# Load the Tensorflow model into memory.
	detection_graph = tf.Graph()
	with detection_graph.as_default():
		od_graph_def = tf.GraphDef()
		with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
			serialized_graph = fid.read()
			od_graph_def.ParseFromString(serialized_graph)
			tf.import_graph_def(od_graph_def, name='')

		sess = tf.Session(graph=detection_graph)

	# print('Model loaded!!!', model_path)

	return sess, detection_graph, category_index


"""def Predict(sess,input_frame):
	image = cv2.imread(self.image)
	image_expanded = np.expand_dims(image, axis=0)

	# Perform the actual detection by running the model with the image as input
	(boxes, scores, classes, num) = self.sess.run(
		[detection_boxes, detection_scores, detection_classes, num_detections],
		feed_dict={image_tensor: image_expanded})

	taco =[category_index.get(value)['name'] for index,value in enumerate(classes[0])if scores[0,index]>0.5]
	print(taco)
	
	# Draw the results of the detection (aka 'visulaize the results')

	vis_util.visualize_boxes_and_labels_on_image_array(
		image,
		np.squeeze(boxes),
		np.squeeze(classes).astype(np.int32),
		np.squeeze(scores),
		self.category_index,
		use_normalized_coordinates=True,
		line_thickness=3,
		min_score_thresh = min_threshold)
	
		"""

@singleton
class Pillar_part():
	def __init__(self, num_classes = 10, img_size = (1280, 600), min_threshold = 0.90):
		self.num_classes = num_classes
		sess, detection_graph, category_index = load_detector(os.path.join(CURRENT_DIRECTORY, PILLAR_PART_MODELS_PATH), self.num_classes)
		self.sess = sess
		self.detection_graph = detection_graph
		self.min_threshold = min_threshold
		self.category_index = category_index
		self.taco = None
		self.predicted_frame = None
		self.predictions = {}
		self.predictions_two = {}
		self.predicted_taco = []
		self.meta = None
		self.defects_list = []
		self.taco_fail = {}

	def inference(self, input_frame):
		self.predictions_two.clear()
		self.predicted_taco.clear()
		self.defects_list.clear()
		self.taco_fail.clear()
		

		# image = cv2.imread(input_frame)
		image = input_frame
		image_expanded = np.expand_dims(image, axis=0)
		print("Inside Pillar Part model")

		# Define input and output tensors (i.e. data) for the object detection classifier
		# Input tensor is the imageqq
		image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

		# Output tensors are the detection boxes, scores, and classes
		# Each box represents a part of the image where a particular object was detected
		detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represents level of confidence for each of the objects.
		# The score is shown on the result image, together with the class label.
		detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

		# Number of objects detected
		num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

		# Perform the actual detection by running the model with the image as input
		(boxes, scores, classes, num) = self.sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections],
			feed_dict={image_tensor: image_expanded})

		self.meta = (boxes, scores, classes, num) 
		CacheHelper().set_json({"Pillar_part" : (boxes, scores, classes, num)})
		self.taco =[self.category_index.get(value)['name'] for index,value in enumerate(classes[0])if scores[0,index]> self.min_threshold]
		print("Pillar_Part_Predicted_TACO", self.taco)

		if bool(self.taco):
			for features in self.taco:
				if features in self.predictions_two:
					self.predictions_two[features] = self.predictions_two[features] + 1
				else:
					self.predictions_two[features] = 1
		
		for features, count in self.predictions_two.items():
			if (features != "Shot_Shot_Presence") and (features != "Clip_Absence") and (features != "Felt_Absence"):
				self.predictions["feature_name"] = features
				self.predictions["count"] = count
				pred = self.predictions.copy()
				self.predicted_taco.append(pred	)

			elif features == "Shot_Shot_Presence":
				self.defects_list.append(features)

			else:
				self.taco_fail.update({features : count})
				
		print("Predictions and Their count>>>>>>>>", self.predictions_two)
		print("Predicted taco from detector module>>>>", self.predicted_taco)
		print("Defects_list from Detector modeule>>>>>", self.defects_list)
		print('Taco_fail from the Detector module>>>>>', self.taco_fail)
		print('Self prediction from detector module', self.predictions)



		self.predicted_frame = vis_util.visualize_boxes_and_labels_on_image_array(
																				image,
																				np.squeeze(boxes),
																				np.squeeze(classes).astype(np.int32),
																				np.squeeze(scores),
																				self.category_index,
																				use_normalized_coordinates=True,
																				line_thickness=3,
																				min_score_thresh = self.min_threshold)
		

		# self.predictions_two.clear()
		# del self.predictions_two
		# cv2.imshow("A",image)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()

@singleton
class Roof_part():
	def __init__(self, num_classes = 10, img_size = (1280, 600), min_threshold = 0.94):
		self.num_classes = num_classes
		sess, detection_graph, category_index = load_detector(os.path.join(CURRENT_DIRECTORY, ROOF_PART_MODELS_PATH), self.num_classes)
		self.sess = sess
		self.detection_graph = detection_graph
		self.min_threshold = min_threshold
		self.category_index = category_index
		self.taco = None
		self.predicted_frame = None
		self.predictions = {}
		self.predictions_two = {}
		self.predicted_taco = []
		self.meta = None
		self.defects_list = []
		self.taco_fail = {}

	def inference(self, input_frame):
		self.predictions_two.clear()
		self.predicted_taco.clear()
		self.defects_list.clear()
		self.taco_fail.clear()
		

		# image = cv2.imread(input_frame)
		image = input_frame
		image_expanded = np.expand_dims(image, axis=0)
		print("Inside Pillar Part model")

		# Define input and output tensors (i.e. data) for the object detection classifier
		# Input tensor is the imageqq
		image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

		# Output tensors are the detection boxes, scores, and classes
		# Each box represents a part of the image where a particular object was detected
		detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represents level of confidence for each of the objects.
		# The score is shown on the result image, together with the class label.
		detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

		# Number of objects detected
		num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

		# Perform the actual detection by running the model with the image as input
		(boxes, scores, classes, num) = self.sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections],
			feed_dict={image_tensor: image_expanded})

		self.meta = (boxes, scores, classes, num) 
		CacheHelper().set_json({"Roof_part" : (boxes, scores, classes, num)})
		self.taco =[self.category_index.get(value)['name'] for index,value in enumerate(classes[0])if scores[0,index]> self.min_threshold]
		print("Roof_Part_Predicted_TACO", self.taco)

		if bool(self.taco):
			for features in self.taco:
				if features in self.predictions_two:
					self.predictions_two[features] = self.predictions_two[features] + 1
				else:
					self.predictions_two[features] = 1
		
		for features, count in self.predictions_two.items():
			if (features != "Shot_Shot_Presence") and (features != "Clip_Absence") and (features != "Felt_Absence") and (features != "Black_Clip_Absence"):
				self.predictions["feature_name"] = features
				self.predictions["count"] = count
				pred = self.predictions.copy()
				self.predicted_taco.append(pred	)

			elif features == "Shot_Shot_Presence":
				self.defects_list.append(features)

			else:
				self.taco_fail.update({features : count})
				
		print("Predictions and Their count>>>>>>>>", self.predictions_two)
		print("Predicted taco from detector module>>>>", self.predicted_taco)
		print("Defects_list from Detector modeule>>>>>", self.defects_list)
		print('Taco_fail from the Detector module>>>>>', self.taco_fail)
		print('Self prediction from detector module', self.predictions)



		self.predicted_frame = vis_util.visualize_boxes_and_labels_on_image_array(
																				image,
																				np.squeeze(boxes),
																				np.squeeze(classes).astype(np.int32),
																				np.squeeze(scores),
																				self.category_index,
																				use_normalized_coordinates=True,
																				line_thickness=3,
																				min_score_thresh = self.min_threshold)
		

		# self.predictions_two.clear()
		# del self.predictions_two
		# cv2.imshow("A",image)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()

@singleton
class Pillar_part_presence_abs():
	def __init__(self, num_classes = 2, img_size = (1280, 720), min_threshold = 0.80):
		self.num_classes = num_classes
		sess, detection_graph, category_index = load_detector(os.path.join(CURRENT_DIRECTORY, PILLAR_PART_PRESENCE_ABSENCE), self.num_classes)
		self.sess = sess
		self.detection_graph = detection_graph
		self.min_threshold = min_threshold
		self.category_index = category_index
		self.taco = None
		self.predicted_frame = None
		self.predictions = {}
		self.predictions_two = {}


	def inference(self, input_frame):

		image = input_frame
		# image = cv2.imread(input_frame)
		image_expanded = np.expand_dims(image, axis=0)

		# Define input and output tensors (i.e. data) for the object detection classifier
		# Input tensor is the imageqq
		image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

		# Output tensors are the detection boxes, scores, and classes
		# Each box represents a part of the image where a particular object was detected
		detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represents level of confidence for each of the objects.
		# The score is shown on the result image, together with the class label.
		detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

		# Number of objects detected
		num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

		# Perform the actual detection by running the model with the image as input
		(boxes, scores, classes, num) = self.sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections],
			feed_dict={image_tensor: image_expanded})
		CacheHelper().set_json({"Pillar_part_presence_abs" : (boxes, scores, classes, num)})
		self.taco =[self.category_index.get(value)['name'] for index,value in enumerate(classes[0])if scores[0,index]>self.min_threshold]
		print("Pillar part Taco>>>>>", self.taco)
		self.meta = (boxes, scores, classes, num) 
		if len(self.taco) > 0: 
			self.predictions['feature_name'] = self.taco[0]
			self.predictions['count'] = self.taco.count(self.taco[0])
			# print("predictions p-p", self.predictions)
		# Draw the results of the detection (aka 'visulaize the results')

		self.predicted_frame = vis_util.visualize_boxes_and_labels_on_image_array(
			image,
			np.squeeze(boxes),
			np.squeeze(classes).astype(np.int32),
			np.squeeze(scores),
			self.category_index,
			use_normalized_coordinates=True,
			line_thickness=3,
			min_score_thresh = self.min_threshold)

"""
@singleton
class Pillar_part_felt():
	def __init__(self, num_classes = 2, img_size = (1280, 720), min_threshold = 0.70):
		self.num_classes = num_classes
		sess, detection_graph, category_index = load_detector(os.path.join(CURRENT_DIRECTORY, PILLAR_PART_FELT_PATH), self.num_classes)
		self.sess = sess
		self.detection_graph = detection_graph
		self.min_threshold = min_threshold
		self.category_index = category_index
		self.taco = None
		self.predicted_frame = None
		self.predictions = {}
		self.predictions_two = {}
		self.meta = None

	def inference(self, input_frame):

		# image = cv2.imread(input_frame)
		image = input_frame
		image_expanded = np.expand_dims(image, axis=0)

		# Define input and output tensors (i.e. data) for the object detection classifier
		# Input tensor is the imageqq
		image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

		# Output tensors are the detection boxes, scores, and classes
		# Each box represents a part of the image where a particular object was detected
		detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represents level of confidence for each of the objects.
		# The score is shown on the result image, together with the class label.
		detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

		# Number of objects detected
		num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

		# Perform the actual detection by running the model with the image as input
		(boxes, scores, classes, num) = self.sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections],
			feed_dict={image_tensor: image_expanded})

		self.meta = (boxes, scores, classes, num) 
		CacheHelper().set_json({"Pillar_part_felt" : (boxes, scores, classes, num)})
		self.taco =[self.category_index.get(value)['name'] for index,value in enumerate(classes[0])if scores[0,index]>0.5]
		# print(self.taco)

		if bool(self.taco): 
			self.predictions['feature_name'] = "Felt_Presence"
			self.predictions['count'] = self.taco.count("Felt_Presence")


		# defect_1 = self.taco.count("Felt_Presence")
		# defect_2 = self.taco.count("Felt_Absence")
		# print(defect_1)
		# print(defect_2)
	
		# Draw the results of the detection (aka 'visulaize the results')

		self.predicted_frame = vis_util.visualize_boxes_and_labels_on_image_array(
																				image,
																				np.squeeze(boxes),
																				np.squeeze(classes).astype(np.int32),
																				np.squeeze(scores),
																				self.category_index,
																				use_normalized_coordinates=True,
																				line_thickness=3,
																				min_score_thresh = self.min_threshold)


		# cv2.imshow("A",image)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()

@singleton
class Pillar_part_clips():
	def __init__(self, num_classes = 2, img_size = (1280, 720), min_threshold = 0.90):
		self.num_classes = num_classes
		sess, detection_graph, category_index = load_detector(os.path.join(CURRENT_DIRECTORY,PILLAR_PART_CLIPS_PATH), self.num_classes)
		self.sess = sess
		self.detection_graph = detection_graph
		self.min_threshold = min_threshold
		self.category_index = category_index
		self.taco = None
		self.predicted_frame = None
		self.predictions = {}
		self.predictions_two = {}
		self.meta = None

	def inference(self, input_frame):

		# image = cv2.imread(input_frame)
		image = input_frame
		image_expanded = np.expand_dims(image, axis=0)

		# Define input and output tensors (i.e. data) for the object detection classifier
		# Input tensor is the imageqq
		image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

		# Output tensors are the detection boxes, scores, and classes
		# Each box represents a part of the image where a particular object was detected
		detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represents level of confidence for each of the objects.
		# The score is shown on the result image, together with the class label.
		detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

		# Number of objects detected
		num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

		# Perform the actual detection by running the model with the image as input
		(boxes, scores, classes, num) = self.sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections],
			feed_dict={image_tensor: image_expanded})
		
		CacheHelper().set_json({"Pillar_part_clips" : (boxes, scores, classes, num)})
		self.meta = (boxes, scores, classes, num) 
		self.taco =[self.category_index.get(value)['name'] for index,value in enumerate(classes[0])if scores[0,index]>0.5]
		# print(self.taco)
		
		
		if bool(self.taco) > 0: 
			self.predictions['feature_name'] = "Clip_Presence"
			self.predictions['count'] = self.taco.count("Clip_Presence")

		# good_1 = self.taco.count("Clip_Presence")
		# # defect_1 = self.taco.count("Clip_Absence")
		# print(good_1)
		# print(defect_1)
	
		# Draw the results of the detection (aka 'visulaize the results')

		self.predicted_frame = vis_util.visualize_boxes_and_labels_on_image_array(
																					image,
																					np.squeeze(boxes),
																					np.squeeze(classes).astype(np.int32),
																					np.squeeze(scores),
																					self.category_index,
																					use_normalized_coordinates=True,
																					line_thickness=3,
																					min_score_thresh = self.min_threshold)	

		# cv2.imshow("a",image)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()		

@singleton
class Pillar_part_shot_shot():
	def __init__(self, num_classes = 2, img_size = (1280, 720), min_threshold = 0.90):
		self.num_classes = num_classes
		sess, detection_graph, category_index = load_detector(os.path.join(CURRENT_DIRECTORY,PILLAR_PART_SHOTSHOT_PATH), self.num_classes)
		self.sess = sess
		self.detection_graph = detection_graph
		self.min_threshold = min_threshold
		self.category_index = category_index
		self.taco = None
		self.predicted_frame = None
		self.predictions = {}
		self.predictions_two = {}
		self.meta = None

	def inference(self, input_frame):

		# image = cv2.imread(input_frame)
		image = input_frame
		image_expanded = np.expand_dims(image, axis=0)

		# Define input and output tensors (i.e. data) for the object detection classifier
		# Input tensor is the imageqq
		image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

		# Output tensors are the detection boxes, scores, and classes
		# Each box represents a part of the image where a particular object was detected
		detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represents level of confidence for each of the objects.
		# The score is shown on the result image, together with the class label.
		detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

		# Number of objects detected
		num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

		# Perform the actual detection by running the model with the image as input
		(boxes, scores, classes, num) = self.sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections],
			feed_dict={image_tensor: image_expanded})
		CacheHelper().set_json({"Pillar_part_shot_shot" : (boxes, scores, classes, num)})
		self.taco =[self.category_index.get(value)['name'] for index,value in enumerate(classes[0])if scores[0,index]>0.3]
		print(self.taco)
		print("inside Pillar_part_shot_shot")
		self.meta = (boxes, scores, classes, num) 
		if len(self.taco) > 0: 
			self.predictions['feature_name'] = "Shot_Shot_Absence"
			self.predictions['count'] = self.taco.count("Shot_Shot_Absence")

	
		# Draw the results of the detection (aka 'visulaize the results')

		self.predicted_frame = vis_util.visualize_boxes_and_labels_on_image_array(
			image,
			np.squeeze(boxes),
			np.squeeze(classes).astype(np.int32),
			np.squeeze(scores),
			self.category_index,
			use_normalized_coordinates=True,
			line_thickness=3,
			min_score_thresh = self.min_threshold)


		# cv2.imshow("A",image)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()

@singleton
class Pillar_part_segregation():
	def __init__(self, num_classes = 4, img_size = (1280, 720), min_threshold = 0.80):
		self.num_classes = num_classes
		sess, detection_graph, category_index = load_detector(os.path.join(CURRENT_DIRECTORY, PILLAR_PART_SEGREGATION_PATH), self.num_classes)
		self.sess = sess
		self.detection_graph = detection_graph
		self.min_threshold = min_threshold
		self.category_index = category_index
		self.taco = None
		self.predicted_frame = None
		self.predictions = {}
		self.predictions_two = {}
		self.meta = None

	def inference(self, input_frame):

		image = input_frame
		image_expanded = np.expand_dims(image, axis=0)

		# Define input and output tensors (i.e. data) for the object detection classifier
		# Input tensor is the imageqq
		image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

		# Output tensors are the detection boxes, scores, and classes
		# Each box represents a part of the image where a particular object was detected
		detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represents level of confidence for each of the objects.
		# The score is shown on the result image, together with the class label.
		detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

		# Number of objects detected
		num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

		# Perform the actual detection by running the model with the image as input
		(boxes, scores, classes, num) = self.sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections],
			feed_dict={image_tensor: image_expanded})
		# print("here", classes[0])
		CacheHelper().set_json({"Pillar_part_segregation" : (boxes, scores, classes, num)})
		self.taco =[self.category_index.get(value)['name'] for index,value in enumerate(classes[0])if scores[0,index]>0.5]
		# print(self.taco)

		self.meta = (boxes, scores, classes, num) 
		if len(self.taco) > 0: 
			self.predictions['feature_name'] = self.taco[0]
			self.predictions['count'] = self.taco.count(self.taco[0])

	
		# Draw the results of the detection (aka 'visulaize the results')

		self.predicted_frame = vis_util.visualize_boxes_and_labels_on_image_array(
			image,
			np.squeeze(boxes),
			np.squeeze(classes).astype(np.int32),
			np.squeeze(scores),
			self.category_index,
			use_normalized_coordinates=True,
			line_thickness=3,
			min_score_thresh = self.min_threshold)

		

		# cv2.imshow("A",image)
		# cv2.waitKey(0)
		# cv2.destroyAllWindows()


@singleton
class Roof_part_wclips():
	def __init__(self, num_classes = 2, img_size = (1280, 720), min_threshold = 0.80):
		self.num_classes = num_classes
		sess, detection_graph, category_index = load_detector(os.path.join(CURRENT_DIRECTORY, ROOF_PART_WCLIPS_PATH), self.num_classes)
		self.sess = sess
		self.detection_graph = detection_graph
		self.min_threshold = min_threshold
		self.category_index = category_index
		self.taco = None
		self.predicted_frame = None
		self.predictions = {}
		self.predictions_two = {}


	def inference(self, input_frame):

		image = input_frame
		# image = cv2.imread(input_frame)
		image_expanded = np.expand_dims(image, axis=0)

		# Define input and output tensors (i.e. data) for the object detection classifier
		# Input tensor is the imageqq
		image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

		# Output tensors are the detection boxes, scores, and classes
		# Each box represents a part of the image where a particular object was detected
		detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represents level of confidence for each of the objects.
		# The score is shown on the result image, together with the class label.
		detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

		# Number of objects detected
		num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

		# Perform the actual detection by running the model with the image as input
		(boxes, scores, classes, num) = self.sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections],
			feed_dict={image_tensor: image_expanded})
		CacheHelper().set_json({"Roof_part_wclips" : (boxes, scores, classes, num)})
		self.taco =[self.category_index.get(value)['name'] for index,value in enumerate(classes[0])if scores[0,index]>self.min_threshold]
		# print(self.taco)
		self.meta = (boxes, scores, classes, num) 

		if len(self.taco) > 0: 
			self.predictions['feature_name'] = "Clip_Presence"
			self.predictions['count'] = self.taco.count("Clip_Presence")
		# Draw the results of the detection (aka 'visulaize the results')

		self.predicted_frame = vis_util.visualize_boxes_and_labels_on_image_array(
			image,
			np.squeeze(boxes),
			np.squeeze(classes).astype(np.int32),
			np.squeeze(scores),
			self.category_index,
			use_normalized_coordinates=True,
			line_thickness=3,
			min_score_thresh = self.min_threshold)



@singleton
class Roof_part_bclips_felt():
	def __init__(self, num_classes = 4, img_size = (1280, 720), min_threshold = 0.80):
		self.num_classes = num_classes
		sess, detection_graph, category_index = load_detector(os.path.join(CURRENT_DIRECTORY, ROOF_PART_BCLIPS_FELT_PATH), self.num_classes)
		self.sess = sess
		self.detection_graph = detection_graph
		self.min_threshold = min_threshold
		self.category_index = category_index
		self.taco = None
		self.predicted_frame = None
		self.predictions = {}
		self.predictions_two = {}


	def inference(self, input_frame):

		image = input_frame
		# image = cv2.imread(input_frame)
		image_expanded = np.expand_dims(image, axis=0)

		# Define input and output tensors (i.e. data) for the object detection classifier
		# Input tensor is the imageqq
		image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

		# Output tensors are the detection boxes, scores, and classes
		# Each box represents a part of the image where a particular object was detected
		detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represents level of confidence for each of the objects.
		# The score is shown on the result image, together with the class label.
		detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

		# Number of objects detected
		num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

		# Perform the actual detection by running the model with the image as input
		(boxes, scores, classes, num) = self.sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections],
			feed_dict={image_tensor: image_expanded})
		CacheHelper().set_json({"Roof_part_bclips_felt" : (boxes, scores, classes, num)})
		self.taco =[self.category_index.get(value)['name'] for index,value in enumerate(classes[0])if scores[0,index]>self.min_threshold]
		# print(self.taco)
		self.meta = (boxes, scores, classes, num) 
		
		if len(self.taco) > 0: 
			self.predictions['feature_name'] = "Black_Clip_Presence"
			self.predictions['count'] = self.taco.count("Black_Clip_Presence")
			self.predictions_two['feature_name'] = "Felt_Presence"
			self.predictions_two['count'] = self.taco.count("Felt_Presence")
		# Draw the results of the detection (aka 'visulaize the results')

		self.predicted_frame = vis_util.visualize_boxes_and_labels_on_image_array(
			image,
			np.squeeze(boxes),
			np.squeeze(classes).astype(np.int32),
			np.squeeze(scores),
			self.category_index,
			use_normalized_coordinates=True,
			line_thickness=3,
			min_score_thresh = self.min_threshold)


@singleton
class Roof_part_segregation():
	def __init__(self, num_classes = 2, img_size = (1280, 720), min_threshold = 0.95):
		self.num_classes = num_classes
		sess, detection_graph, category_index = load_detector(os.path.join(CURRENT_DIRECTORY, ROOF_PART_SEGREGATION_PATH), self.num_classes)
		self.sess = sess
		self.detection_graph = detection_graph
		self.min_threshold = min_threshold
		self.category_index = category_index
		self.taco = None
		self.predicted_frame = None
		self.predictions = {}
		self.predictions_two = {}


	def inference(self, input_frame):

		image = input_frame
		# image = cv2.imread(input_frame)
		image_expanded = np.expand_dims(image, axis=0)

		# Define input and output tensors (i.e. data) for the object detection classifier
		# Input tensor is the imageqq
		image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

		# Output tensors are the detection boxes, scores, and classes
		# Each box represents a part of the image where a particular object was detected
		detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represents level of confidence for each of the objects.
		# The score is shown on the result image, together with the class label.
		detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

		# Number of objects detected
		num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

		# Perform the actual detection by running the model with the image as input
		(boxes, scores, classes, num) = self.sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections],
			feed_dict={image_tensor: image_expanded})
		CacheHelper().set_json({"Roof_part_segregation" : (boxes, scores, classes, num)})
		self.taco =[self.category_index.get(value)['name'] for index,value in enumerate(classes[0])if scores[0,index]>self.min_threshold]
		# print(self.taco)
		self.meta = (boxes, scores, classes, num) 
		if len(self.taco) > 0: 
			self.predictions['feature_name'] = self.taco[0]
			self.predictions['count'] = self.taco.count(self.taco[0])
		# Draw the results of the detection (aka 'visulaize the results')

		self.predicted_frame = vis_util.visualize_boxes_and_labels_on_image_array(
			image,
			np.squeeze(boxes),
			np.squeeze(classes).astype(np.int32),
			np.squeeze(scores),
			self.category_index,
			use_normalized_coordinates=True,
			line_thickness=3,
			min_score_thresh = self.min_threshold)


@singleton
class Roof_part_shot_shot():
	def __init__(self, num_classes = 2, img_size = (1280, 720), min_threshold = 0.91):
		self.num_classes = num_classes
		sess, detection_graph, category_index = load_detector(os.path.join(CURRENT_DIRECTORY, ROOF_PART_SHOTSHOT_PATH), self.num_classes)
		self.sess = sess
		self.detection_graph = detection_graph
		self.min_threshold = min_threshold
		self.category_index = category_index
		self.taco = None
		self.predicted_frame = None
		self.predictions = {}
		self.predictions_two = {}


	def inference(self, input_frame):

		image = input_frame
		# image = cv2.imread(input_frame)
		image_expanded = np.expand_dims(image, axis=0)

		# Define input and output tensors (i.e. data) for the object detection classifier
		# Input tensor is the imageqq
		image_tensor = self.detection_graph.get_tensor_by_name('image_tensor:0')

		# Output tensors are the detection boxes, scores, and classes
		# Each box represents a part of the image where a particular object was detected
		detection_boxes = self.detection_graph.get_tensor_by_name('detection_boxes:0')

		# Each score represents level of confidence for each of the objects.
		# The score is shown on the result image, together with the class label.
		detection_scores = self.detection_graph.get_tensor_by_name('detection_scores:0')
		detection_classes = self.detection_graph.get_tensor_by_name('detection_classes:0')

		# Number of objects detected
		num_detections = self.detection_graph.get_tensor_by_name('num_detections:0')

		# Perform the actual detection by running the model with the image as input
		(boxes, scores, classes, num) = self.sess.run(
			[detection_boxes, detection_scores, detection_classes, num_detections],
			feed_dict={image_tensor: image_expanded})
		CacheHelper().set_json({"Roof_part_shot_shot" : (boxes, scores, classes, num)})
		self.taco =[self.category_index.get(value)['name'] for index,value in enumerate(classes[0])if scores[0,index]>self.min_threshold]
		# print(self.taco)
		self.meta = (boxes, scores, classes, num) 
		if len(self.taco) > 0: 
			self.predictions['feature_name'] = "Shot_Shot_Absence"
			self.predictions['count'] = self.taco.count("Shot_Shot_Absence")

		# Draw the results of the detection (aka 'visulaize the results')
		self.predicted_frame = vis_util.visualize_boxes_and_labels_on_image_array(
			image,
			np.squeeze(boxes),
			np.squeeze(classes).astype(np.int32),
			np.squeeze(scores),
			self.category_index,
			use_normalized_coordinates=True,
			line_thickness=3,
			min_score_thresh = self.min_threshold)"""


# if __name__ == "__main__":
	# detect = Pillar_part_felt()
	# detect = Pillar_part_clips()
	# detect = Pillar_part_segregation()
	# detect.inference()