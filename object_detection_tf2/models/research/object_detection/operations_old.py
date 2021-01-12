""" This is the older codebase"""

import os
import sys
# import pandas as pd
import json
import tensorflow as tf
from google.protobuf import text_format
from object_detection.protos import pipeline_pb2
# input_dir_path = r"/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/mount_directory"
input_dir_path = r"/var_data2"
model_config_file_path = r"/var_data/models/research/object_detection/training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/pipeline.config"

for i in os.listdir(input_dir_path):
    # print(i)
    if i.split('.')[-1] == "json":
        json_path = os.path.join(input_dir_path,i)
        # print(json_path)
    else:
        if os.path.isdir(os.path.join(input_dir_path,i)):
            for j in os.listdir(os.path.join(input_dir_path,i)):
                if j == 'train':
                    train_dir_path =os.path.join(input_dir_path,i,j)
                    print(train_dir_path)

#Logic --> For manipulating the config file parameters 

# import pandas as pd
with open(json_path) as f:
  data = json.load(f)
  
print(data['BATCH_SIZE'])  

def protos_read_file():
    structure_config = pipeline_pb2.TrainEvalPipelineConfig()                                                                                                                                                                                                          
    with tf.io.gfile.GFile(model_config_file_path, "r") as f:                                                                                                                                                                                                                     
        proto_str = f.read()                                                                                                                                                                                                                                          
        text_format.Merge(proto_str, structure_config)
    return structure_config

def protos_write_file(structure_config):
    config_text = text_format.MessageToString(structure_config)                                                                                                                                                                                                        
    with tf.io.gfile.GFile(model_config_file_path, "wb") as f:                                                                                                                                                                                                                       
        f.write(config_text)

def protos_modify_file(structure_config):
    structure_config.model.faster_rcnn.num_classes = data['NO_OF_CLASSES']
    structure_config.train_config.fine_tune_checkpoint_type = 'detection'
    structure_config.train_config.num_steps = data['STEPS']

    structure_config.train_config.fine_tune_checkpoint = '/var_data/models/research/object_detection/training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/checkpoint/ckpt-0'
    structure_config.train_input_reader.label_map_path = '/var_data/models/research/object_detection/training/label_map.pbtxt'
    structure_config.train_input_reader.tf_record_input_reader.input_path[0] = '/var_data/models/research/object_detection/train.record'

    structure_config.train_config.batch_size = data['BATCH_SIZE']

    structure_config.train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate.learning_rate_base = data['LR']
    # structure_config.eval_input_reader[0].label_map_path = '/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/training/label_map.pbtxt'
    # structure_config.eval_input_reader[0].tf_record_input_reader.input_path[0] = 'test.record'

    return structure_config


def protos_setup():
    structure_config = protos_read_file()
    structure_config = protos_modify_file(structure_config)
    protos_write_file(structure_config)

protos_setup()

# Logic for creatig labelmap.pbtxt

Classes_map = data['CLASSES']
print(Classes_map)

def create_labelmap():
    with open('/var_data/models/research/object_detection/training/label_map.pbtxt', 'a') as the_file:
        counter = 0
        for i in Classes_map:
            counter = counter + 1
            the_file.write('item\n')
            the_file.write('{\n')
            the_file.write('id :{}'.format(int(counter)))
            the_file.write('\n')
            the_file.write("name :'{0}'".format(str(i)))
            the_file.write('\n')
            the_file.write('}\n')

create_labelmap()



# create the tensorflow records
 
#command  = "python3 generate_tfrecords.py  -x /media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/mount_directory/images -l /media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/training/label_map.pbtxt -o /media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/train.record"
command  = "python generate_tfrecords.py  -x /var_data2/images -l /var_data/models/research/object_detection/training/label_map.pbtxt -o /var_data/models/research/object_detection/train.record"

os.system(command)


# Triggering training 
saving_train_data = os.path.join(input_dir_path,"training_data")
if not os.path.exists(saving_train_data):
    os.mkdir(saving_train_data)

# train_command  = "python3 model_main_tf2.py --model_dir=" + saving_train_data+"--pipeline_config_path=/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/pipeline.config"

train_command  = "python3 model_main_tf2.py --model_dir=" + saving_train_data+" "+"--pipeline_config_path=/var_data/models/research/object_detection/training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/pipeline.config"


os.system(train_command)

