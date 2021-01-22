import os
import sys
import pandas as pd
import json
import tensorflow as tf
from google.protobuf import text_format
from object_detection.protos import pipeline_pb2
import numpy as np
import random
import pymongo
from pymongo import MongoClient
import json
from bson.objectid import ObjectId
import cv2
from pprint import pprint
from shutil import copyfile

def create_paths():
    input_dir_path = r"/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/mount_directory"
    model_config_file_path = r"/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/pipeline.config"
    retrain_cofig = r"/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/retrain_config.config"
    return input_dir_path,model_config_file_path,retrain_cofig
#Logic --> For manipulating the config file parameters 


def data_base_op():
    # img height, width
    image_dir = os.path.join(input_dir_path,"images")
    for i in os.listdir(image_dir):
      image_path = os.path.join(image_dir,i)
      img_arr = cv2.imread(image_path)
      height, width, depth = img_arr.shape
   # def mongo cleint   
    # client = MongoClient('localhost',27017)
 
    #def parts database
    parts_db = client["parts_database"]   
    parts_coll = parts_db["parts"]

   # above line should be commentetd before dockerising
    if not parts_coll.countDocuments == 0:
      parts_coll.drop()
    with open(os.path.join(input_dir_path,"parts.json")) as f:
        data = json.load(f)
    parts_info = parts_coll.insert_many(data)       
    cursor = parts_coll.find({})
  ################## Annotations ##################
    anno_db = client["anno_database"]
    anno_coll = anno_db["annotations"]
    if not anno_coll.countDocuments == 0:
      anno_coll.drop()
    with open(os.path.join(input_dir_path,"6001593414c693a204021ea4.json")) as fp:
      anno_data= json.load(fp)
    
    # print(anno_data)
    anno_info = anno_coll.insert_many(anno_data) 
    # from pprint import pprint
    cursor = anno_coll.find()
    df = pd.DataFrame(columns = ['filename', 'width', 'height','class','xmin','ymin','xmax','ymax']) 
    for document in cursor: 
        # print(document["file_path"])
        if document["state"] == "tagged":
          print("inside loop")
          file_path = document["file_path"]
          file_name = file_path.split('/')[-1]
          x0 = document["regions"][0]["x"] * width
          y0 = document["regions"][0]["y"]*height
          x1 = (document["regions"][0]["w"] + document["regions"][0]["x"]) * width
          y1 = (document["regions"][0]["h"] + document["regions"][0]["y"]) * height
          class_var = document["regions"][0]["cls"]
          df = df.append({'filename' :str(file_name),'width' :str(int(width)),'height' :str(int(height)),'class':str(class_var),'xmin':str(int(x0)),'ymin':str(int(y0)),'xmax':str(int(x1)),'ymax':str(int(y1))},ignore_index="True")

    # print(df)
    msk = np.random.rand(len(df)) < 0.8
    train_df = df[msk]
    test_df = df[~msk]
    csv_base_path = "/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/images"
    if not os.path.exists(csv_base_path):
        os.mkdir(csv_base_path)

    train_df.to_csv(os.path.join(csv_base_path,"train_labels.csv"), index=False)
    test_df.to_csv(os.path.join(csv_base_path, "test_labels.csv"),index=False)

    print(df["class"].unique())
    class_list = df["class"].unique()
    no_of_cls = len(class_list)

    return class_list,no_of_cls,csv_base_path

def modify_tf_records(class_list):
  base_generate_re_path = r"/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/generate_tfrecord_base.py"
  final_tf =  r"/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/modified_tf_records.py"
  generate_tf_record = ''

#   print(type(temp_list))
  copyfile(base_generate_re_path, final_tf)
  for idx, value in enumerate(class_list):
          print("value",value)
          first_class = '''    
    if row_label == 'first':
        return 1
                  '''
          all_other_class = '''
    elif row_label == 'other':
        return 2 
'''
  
          if idx == 0:
              to_append = first_class.replace('first',value)
          else:
              to_append = all_other_class.replace('other',value).replace('2',str(idx+1))

          generate_tf_record+=to_append

#   print(generate_tf_record)
  with open(final_tf) as f:
      lines = f.readlines()

    # custom_tf_record_path = os.path.join(config_save_path,'generate_tfrecord.py')
  with open(final_tf, "w") as f:
      lines.insert(37, generate_tf_record)
      f.write("".join(lines))

    # print('Done: Edited generate_tfrecord.py')

def create_experiment_collection():
#   client = MongoClient('localhost',27017)
  exp_db = client["experiment_database"]
  exp_collection = exp_db["exp_collection"]


  if not exp_collection.countDocuments == 0:
    exp_collection.drop()

  exp_dict = {
              "exp_no" : 123,
              "hyperparameters":{
                "BATCH_SIZE" : 1,
                "LR" : 0.04,
                "STEPS" : 100
              },
              "RETRAIN": True,
              "STATUS" : "Initialized",
              "history":{

              }

        }  
  exp_info = exp_collection.insert_one(exp_dict) 
    # from pprint import pprint
  cursor = exp_collection.find()
  for val in cursor:
    batch_size = val["hyperparameters"]["BATCH_SIZE"]
    lr = val["hyperparameters"]["LR"]
    no_steps = val["hyperparameters"]["STEPS"]
    training_status = val["RETRAIN"]
  return batch_size,lr,no_steps,exp_collection,training_status

def protos_read_file(sample_config):
    structure_config = pipeline_pb2.TrainEvalPipelineConfig()                                                                                                                                                                                                          
    with tf.io.gfile.GFile(model_config_file_path, "r") as f:                                                                                                                                                                                                                     
        proto_str = f.read()                                                                                                                                                                                                                                          
        text_format.Merge(proto_str, structure_config)
    return structure_config

def protos_write_file(structure_config):
    config_text = text_format.MessageToString(structure_config)                                                                                                                                                                                                        
    with tf.io.gfile.GFile(model_config_file_path, "wb") as f:                                                                                                                                                                                                                       
        f.write(config_text)

def protos_modify_file(structure_config,no_of_cls,batch_size,lr,no_steps,training_status):
    structure_config.model.faster_rcnn.num_classes = no_of_cls
    structure_config.train_config.fine_tune_checkpoint_type = 'detection'
    structure_config.train_config.num_steps = no_steps
    structure_config.train_config.fine_tune_checkpoint = '/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/checkpoint/ckpt-0'
    structure_config.train_input_reader.label_map_path = '/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/training/label_map.pbtxt'
    structure_config.train_input_reader.tf_record_input_reader.input_path[0] = '/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/train.record'
    # structure_config.eval_input_reader.label_map_path = '/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/training/label_map.pbtxt'
    # structure_config.eval_input_reader.tf_record_input_reader.input_path[0] = '/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/test.record'
    structure_config.train_config.batch_size = batch_size
    structure_config.train_config.optimizer.momentum_optimizer.learning_rate.cosine_decay_learning_rate.learning_rate_base = lr    
    # if training_status == True:
    #   structure_config.train_config.freeze_variables = ".*FeatureExtractor."


    # if training_status == True:
    #   with open(model_config_file_path) as f:
    #     lines = f.readlines()

    #   freeze_var = "freeze_variables:.*FeatureExtractor."
    #       # custom_tf_record_path = os.path.join(config_save_path,'generate_tfrecord.py')
    #   with open(model_config_file_path, "w") as f:
    #         lines.insert(90, freeze_var)
    #         f.write("".join(lines))    


    return structure_config





def protos_read_file_retrain(retrain_cofig):
    structure_config = pipeline_pb2.TrainEvalPipelineConfig()                                                                                                                                                                                                          
    with tf.io.gfile.GFile(retrain_cofig, "r") as f:                                                                                                                                                                                                                     
        proto_str = f.read()                                                                                                                                                                                                                                          
        text_format.Merge(proto_str, structure_config)
    return structure_config

def protos_write_file_retrain(structure_config):
    config_text = text_format.MessageToString(structure_config)                                                                                                                                                                                                        
    with tf.io.gfile.GFile(retrain_cofig, "wb") as f:                                                                                                                                                                                                                       
        f.write(config_text)    

def protos_setup():
    structure_config = protos_read_file(model_config_file_path)
    structure_config = protos_modify_file(structure_config,no_of_cls,batch_size,lr,no_steps,training_status)
    protos_write_file(structure_config)



# Logic for creatig labelmap.pbtxt
def retrain_model(retrain_cofig): 
  # retrain_cofig = "/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/retrain.config"
  
  # copyfile(retrain_cofig, retrain_cofig)
  structure_config = protos_read_file_retrain(retrain_cofig)
  structure_config = protos_modify_file(structure_config,no_of_cls,batch_size,lr,no_steps,training_status)
  protos_write_file_retrain(structure_config)

def create_labelmap(class_list):
    Classes_map = class_list
    # print(Classes_map)
    if os.path.isfile('/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/training/label_map.pbtxt'):
        os.remove('/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/training/label_map.pbtxt')
    with open('/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/training/label_map.pbtxt', 'a') as the_file:
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




def main(input_dir_path,csv_base_path,exp_collection,training_status):
# create the tensorflow records
    command_train  = "python3 modified_tf_records.py  --csv_input="+csv_base_path+"/train_labels.csv --image_dir=/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/mount_directory/images --output_path=/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/train.record"  
    command_test = "python3 modified_tf_records.py  --csv_input="+csv_base_path+"/test_labels.csv --image_dir=/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/mount_directory/images --output_path=/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/test.record" 
    os.system(command_train)
    os.system(command_test)

# Triggering training 
    saving_train_data = os.path.join(input_dir_path,"training_data_host")
    if not os.path.exists(saving_train_data):
        os.mkdir(saving_train_data)
    if training_status != True:
      train_command  = "python3 model_main_tf2.py --model_dir=" + saving_train_data+" "+"--pipeline_config_path=training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/pipeline.config"
    else :
      train_command  = "python3 model_main_tf2.py --model_dir=" + saving_train_data+" "+"--pipeline_config_path=training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/retrain_config.config"
    import time            
    tensorBoardPath = os.path.join(saving_train_data,"train")
    def launchTensorBoard():
        # import os
        # os.system('tensorboard --logdir=' + tensorBoardPath)
        exp_collection.update_many({"STATUS" : "Initialized" }, {"$set" : {"STATUS" :"Running"}})
        os.system("python3 -m tensorboard.main --logdir="+tensorBoardPath)
        #update the query to db
        
        
        return

    # def update_collection():
        
        # return
    import threading
    # t1 = threading.Thread(target=update_collection,args=([]))
    t2 = threading.Thread(target=launchTensorBoard, args=([]))
    t2.start()
    # t1.start()
    # launchTensorBoard()
    os.system(train_command)

    # Code for creating inference_graphs 

    export_command = "python exporter_main_v2.py --input_type image_tensor --pipeline_config_path  training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/retrain_config.config --trained_checkpoint_dir /media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/mount_directory/training_data_host --output_directory /media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/mount_directory/training_data_host/inference_graph"
    os.system(export_command)

    print("Inferencing is completed")


    #code for updating evaluation  metrics
    eval_results = "/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/models_tf2_backup/models/research/object_detection/eval_results.txt"
    f = open(eval_results, "w")

    if training_status != True:
      comm = "python model_main_tf2.py --alsologtostderr  --model_dir=training/  --pipeline_config_path=training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/pipeline.config   --checkpoint_dir=/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/mount_directory/training_data_host_old   --eval_timeout=0"
      os.system(comm + ' > '+eval_results)
    else:
      comm = "python model_main_tf2.py --alsologtostderr  --model_dir=training/  --pipeline_config_path=training/faster_rcnn_resnet50_v1_1024x1024_coco17_tpu-8/retrain_config.config   --checkpoint_dir=/media/snehal/2c6e57b3-ed0c-4926-a4e1-fca4d64a4386/snehal/mount_directory/training_data_host   --eval_timeout=0"
      os.system(comm + ' > '+eval_results)       
    

    file1 = open(eval_results, 'r') 
    Lines = file1.readlines() 
      
    count = 0
    # Strips the newline character 
    list_temp = []
    for line in Lines:
        list_temp.append(line) 
    file1.close()    
        # print(line[0]["PascalBoxes_Precision/mAP@0.5IOU"])
        # print("Line{}: {}".format(count, line.strip())) 
    print(list_temp[0].split("{")[-1].split(',')[0])

    metric_value = list_temp[0].split("{")[-1].split(',')[0]
    key = metric_value.split(':')[0]
    value = metric_value.split(':')[-1]

    cursor = exp_collection.find({})
    for document in cursor:
        id_val =document['_id']

    # exp_collection.insert({"metric_type": key, "mAP@ 0_5IOU" : value })

    exp_collection.update_one(
          {"history": {} },
          { "$set": {"history.metric_type": key, "history.mAP@ 0_5IOU" : value } }
        )
    exp_collection.update_many({"STATUS" : "Running" }, {"$set" : {"STATUS" :"Completed"}})    
    # exp_collection.find().close()
    # t2.exit()
    os._exit(1)

    return "done"
# def db_operations():



if __name__ == '__main__':
    client = MongoClient('localhost',27017)
    input_dir_path,model_config_file_path,retrain_cofig = create_paths()
    class_list,no_of_cls,csv_base_path = data_base_op()
    modify_tf_records(class_list)
    batch_size,lr,no_steps,exp_collection,training_status  = create_experiment_collection()

    # data = read_json(json_path)
    # print(data)
    # print(training_status)
    if training_status == True :
      retrain_model(retrain_cofig) 
    else:   
      protos_setup()
    print("done setup")

    create_labelmap(class_list)

    print("labelmap")

    main(input_dir_path,csv_base_path,exp_collection,training_status)
    client.close()
    print("done main")
    
