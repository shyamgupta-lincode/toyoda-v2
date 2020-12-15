export interface WorkstationPayload {
  workstation_name: string;
  camera_config: CameraConfig;
}

export interface Workstation {
  _id: string;
  workstation_name: string;
  camera_config: CameraConfig;
}

export interface CameraConfig {
  cameras: Camera[];
}

export interface Camera {
  camera_name: string;
  camera_id: number;
}

export interface UploadResponse {
  status: string;
  upload_id: string;
}

export interface DatasetPayload {
  part_number: string;
  line_number: string;
  factory_code: string;
  upload_id: string;
}

export interface DatasetResponse {
  status: string;
  data: Dataset;
}

export interface Dataset {
  line_number: string;
  part_number: string;
  data_info: {
    total_labels: number;
    total_data_test: number;
    label_wise_distribution: {
      label_a: {
        test: number;
        train: number;
      };
      label_b: {
        test: number;
        train: number;
      };
      label_c: {
        test: number;
        train: number;
      };
    };
    total_data_train: number;
  };
  datapath: string;
  factory_code: string;
  experiments: [
    {
      opt: string;
      status: string;
      img_size: number;
      augmentations: {
        flip_horizontly: boolean;
        do_flip: boolean;
        zoom: number;
      };
      metrics: [string];
      bs: number;
      dataset_id: string;
      datapath: string;
      experiment_name: string;
      experiment_type: string;
      lr: number;
      experiment_id: string;
      model: string;
    }
  ];
  _id: string;
}

export interface ExperimentPayload {
  experiment_name: string;
  experiment_type: string;
  model_type: string;
  lr: number;
  upload_id: string;
  image_size: number;
  batch_size: number;
  metrics: {
    precision: boolean;
    recall: boolean;
    fOneScore: boolean;
  };
}
