from detector_module import *
    
#Camera service
original_frame_keyholder = 'original-frame'

#PlC service
process_start_keyholder = 'process-start'
process_stop_keyholder = 'process-stop'
part_accepted_keyholder = 'part-accepted'
process_completed = 'one-process-completed'

#Detecor

predicted_frame_keyholder = 'predicted-frame'
final_frame_list_keyholder = 'final-frame-list'

#DB entry 
rescan_keyholder = 'rescan-required'
last_entry_id_keyholder = "last-entry-id"  #curr-inspection-id
current_inspection_id_keyholder = "curr-inspection-id"
# Kanban:

kanban_keyholder = 'kanban'
short_number_keyholder = 'short-number'
part_number_keyholder = 'part-number'

#User_id for the current logged in user in the current client machine.
user_id_keyholder = 'user_id_key'

#worksation_id for the current client machine.
workstation_id_keyholder = 'workstation_id_key'

#planned production count key
production_count_keyholder = 'production_count_key'


## Detector to part_number map


MODEL_MAP = {
    "IG95" : [#Pillar_part_presence_abs,
              Pillar_part_segregation,
              Pillar_part_felt, 
              Pillar_part_clips,
              Pillar_part_shot_shot  
            ],

    "IG96" : [#Pillar_part_presence_abs,
              Pillar_part_segregation,
              Pillar_part_felt, 
              Pillar_part_clips,
              Pillar_part_shot_shot  
            ],        

    "IG97" : [#Pillar_part_presence_abs,
              Pillar_part_segregation,
              Pillar_part_felt, 
              Pillar_part_clips,
              Pillar_part_shot_shot  
            ],

    "IG98" : [#Pillar_part_presence_abs,
              Pillar_part_segregation,
              Pillar_part_felt, 
              Pillar_part_clips,
              Pillar_part_shot_shot  
            ]        
    }
