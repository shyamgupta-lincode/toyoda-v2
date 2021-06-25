import os
# from detector_module import *


#Setting the model path
# CURRENT_DIRECTORY = os.getcwd()
# print("------CURRENT_DIRECTORY-----------", CURRENT_DIRECTORY)
# PILLAR_PART_FELT_PATH = "./models/inference_graph_PP_felt/"
# PILLAR_PART_CLIPS_PATH = "./models/inference_graph_PP_wclips/"
# PILLAR_PART_SEGREGATION_PATH = "./models/inference_graph_PP_Lh_rh_seg/"
# PILLAR_PART_SHOTSHOT_PATH = "./models/inference_graph_PP_shot_shot/"
CURRENT_DIRECTORY = "/home/toyoda/livis_v2_toyota/republic/backend/AI_Controller"
PILLAR_PART_PRESENCE_ABSENCE = "models/inference_graph_Pillar_presence_abs/"
PILLAR_PART_MODELS_PATH = "models/inference_graph_Pillar/"
ROOF_PART_MODELS_PATH = "models/inference_graph_roofside/"
# ROOF_PART_MODELS_PATH = "./models/inference_graph_roofside_rs3/"

PREDICTED_IMAGE_DIRECTORY = './predicted'
ACTUAL_IMAGE_DIRECTORY = "./actual"
# ROOF_PART_WCLIPS_PATH = "./models/inference_graph_roof_wclips/"
# ROOF_PART_SEGREGATION_PATH = "./models/inference_graph_roof_lhrh_seg/"
# ROOF_PART_BCLIPS_FELT_PATH = "./models/inference_graph_roof_bclips_felt/"
# ROOF_PART_SHOTSHOT_PATH = "./models/inference_graph_roof_shot_shot/"

PILLAR_PART_PRESENCE_ABSENCE_THRESHOLD = 0.95
PILLAR_PART_MODEL_THRESHOLD = 0.90
ROOF_PART_MODEL_THRESHOLD = 0.95

TOP_CAMERA_USAGE = ["IG98", "IG97", "IG96", "IG95"] #pillar
SIDE_CAMERA_USAGE = ["IH06", "IH07"] #roof