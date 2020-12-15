import os
# from detector_module import *


#Setting the model path
CURRENT_DIRECTORY = os.getcwd()
print("------CURRENT_DIRECTORY-----------", CURRENT_DIRECTORY)
PILLAR_PART_FELT_PATH = "./models/inference_graph_PP_felt/"
PILLAR_PART_CLIPS_PATH = "./models/inference_graph_PP_wclips/"
PILLAR_PART_SEGREGATION_PATH = "./models/inference_graph_PP_Lh_rh_seg/"
PILLAR_PART_SHOTSHOT_PATH = "./models/inference_graph_PP_shot_shot/"
PILLAR_PART_PRESENCE_ABSENCE = "./models/inference_graph_Pillar_presence_abs/"


# MODEL_MAP = {
#     "IG95" : [#Pillar_part_presence_abs,
#               Pillar_part_segregation,
#               Pillar_part_felt, 
#               Pillar_part_clips,
#               Pillar_part_shot_shot  
#             ],

#     "IG98" : [#Pillar_part_presence_abs,
#               Pillar_part_segregation,
#               Pillar_part_felt, 
#               Pillar_part_clips,
#               Pillar_part_shot_shot  
#             ]        
    # }
