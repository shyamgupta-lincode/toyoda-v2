import os
import sys
import pandas as pd
import json
import tensorflow as tf
from google.protobuf import text_format
from object_detection.protos import pipeline_pb2



def create_paths():
    input_dir_path = r"/var_data2"
    model_config_file_path = r"/var_data/models/research/object_detection/training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/pipeline.config"
    for i in os.listdir(input_dir_path):
        if i.split('.')[-1] == "json":
            json_path = os.path.join(input_dir_path,i)
        # else:
        #     if os.path.isdir(os.path.join(input_dir_path,i)):
        #         for j in os.listdir(os.path.join(input_dir_path,i)):
        #             if j == 'images':
        #                 train_dir_path =os.path.join(input_dir_path,i,j)
        #                 print(train_dir_path)

    return json_path,input_dir_path,model_config_file_path
#Logic --> For manipulating the config file parameters 


def read_json(json_path):
    with open(json_path) as f:
        data = json.load(f)
    return data
# print(data['BATCH_SIZE'])  

def protos_read_file(model_config_file_path):
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


    return structure_config


def protos_setup():
    structure_config = protos_read_file(model_config_file_path)
    structure_config = protos_modify_file(structure_config)
    protos_write_file(structure_config)



# Logic for creatig labelmap.pbtxt



def create_labelmap(data):
    Classes_map = data['CLASSES']
    # print(Classes_map)
    if os.path.isfile('/var_data/models/research/object_detection/training/label_map.pbtxt'):
        os.remove('/var_data/models/research/object_detection/training/label_map.pbtxt')
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




def main(input_dir_path):
# create the tensorflow records
    command  = "python generate_tfrecords.py  -x /var_data2/images -l /var_data/models/research/object_detection/training/label_map.pbtxt -o /var_data/models/research/object_detection/train.record"

    os.system(command)

# Triggering training 
    saving_train_data = os.path.join(input_dir_path,"training_data")
    if not os.path.exists(saving_train_data):
        os.mkdir(saving_train_data)

    train_command  = "python3 model_main_tf2.py --alsologtostderr  --model_dir=" + saving_train_data+" "+"--pipeline_config_path=training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/pipeline.config"
    import time            
    tensorBoardPath = os.path.join(saving_train_data,"train")
    def launchTensorBoard():
        import os
        # os.system('tensorboard --logdir=' + tensorBoardPath)
        os.system("python3 -m tensorboard.main --logdir="+tensorBoardPath)
        return

    import threading
    t2 = threading.Thread(target=launchTensorBoard, args=([]))
    t2.start()
    os.system(train_command)


if __name__ == '__main__':
    json_path,input_dir_path,model_config_file_path = create_paths()
    # print(json_path)
    # print(train_dir_path)
    # print(input_dir_path)
    # print(model_config_file_path)

    data = read_json(json_path)
    # print(data)

    protos_setup()
    # print("done setup")

    create_labelmap(data)

    # print("labelmap")

    main(input_dir_path)
    # print("done main")