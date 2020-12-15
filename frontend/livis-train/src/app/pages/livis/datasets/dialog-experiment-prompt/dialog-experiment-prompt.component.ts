import { Component, OnInit, Input } from '@angular/core';
import { NbDialogRef } from '@nebular/theme';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';

import { LivisService } from '../../livis.service';
import { NbToastrService } from '@nebular/theme';

// import { find, get, pull } from 'lodash';
@Component({
  selector: 'ngx-dialog-experiment-prompt',
  templateUrl: 'dialog-experiment-prompt.component.html',
  styleUrls: ['dialog-experiment-prompt.component.scss'],
  providers: [LivisService],
})
export class DialogExperimentPromptComponent implements OnInit {

  @Input() dataset: any;

  firstForm: FormGroup;
  models = ["ssd_mobilenet_v2_320", "ssd_mobilenet_v1_fpn_640",
  "ssd_mobilenet_v2_fpnlite_320", "ssd_mobilenet_v2_fpnlite_640",
  "ssd_resnet50_v1_fpn_320", "ssd_resnet50_v1_fpn_640",
  "ssd_resnet101_v1_fpn_320", "ssd_resnet101_v1_fpn_640",
  "ssd_resnet152_v1_fpn_320", "ssd_resnet152_v1_fpn_640",
  "faster_rcnn_resnet50_v1_640", "faster_rcnn_resnet50_v1_1024",
  "faster_rcnn_resnet101_v1_640", "faster_rcnn_resnet101_v1_1024",
  "faster_rcnn_resnet152_v1_640", "faster_rcnn_resnet152_v1_1024",
  "faster_rcnn_inception_resnet_v2_640", "faster_rcnn_inception_resnet_v2_1024",
  "efficientdet_d0", "efficientdet_d1", 
  "efficientdet_d2", "efficientdet_d3",
  "efficientdet_d4", "efficientdet_d5",
  "efficientdet_d6", "efficientdet_d7"
  ];

  modelName: string = '';
  tuning: any = {
    batchSize: 2,
    imageSize: 25000,
    lrValue: -1,
  };
  metrics: any = {
    precision: true,
    recall: true,
    fOneScore: true,
  };
  // tags = ["aaa"];
  tags: any[] = [];

  experiment: any = {};


  constructor(protected ref: NbDialogRef<DialogExperimentPromptComponent>, private fb: FormBuilder,
    private toastrService: NbToastrService,) {}

  ngOnInit() {
    this.firstForm = this.fb.group({
      typeOfExperiment: ['', Validators.required],
      name: ['', Validators.required],
      jig_list: ['', []],

      // label_list[]: ['', Validators.required],

    });
  }

  focusTagInput(): void {
    // this.tagInputRef.nativeElement.focus();
  }

  onKeyUp(event: KeyboardEvent): void {
    const inputValue: string = this.firstForm.controls.jig_list.value;
    if (event.code === 'Backspace' && !inputValue) {
      // this.removeTag();
      return;
    } else {
      if (event.code === 'Comma' || event.code === 'Space') {
        this.addTag(inputValue);
        this.firstForm.controls.jig_list.setValue('');
      }
    }
  }

  addTag(tag: string): void {
    this.tags.push(tag);
  }

  removeTag(tag?: any): void {
    let index = this.tags.indexOf(tag);
    if (index >= 0) {
      this.tags.splice(index, 1);
    }
  }

  onFirstSubmit() {
    // console.log(this.firstForm.value);
    // console.log(this.dataset);
    // console.log(Object.keys(this.dataset.label_info.detector_label_data));
    // if(this.tags.length > 0)
    // {
    //   this.firstForm.markAsDirty();
    // }else{
      this.firstForm.markAsDirty();
      // this.tags
    // }
    
  }

  cancel() {
    this.ref.close();
  }

  collectValues() {
    var label_data = [];
    if(this.firstForm.value.typeOfExperiment == "classification")
    {
      label_data  = Object.keys(this.dataset.label_info.classifier_label_data);
    }else if(this.firstForm.value.typeOfExperiment == "detection")
    {
      label_data  = Object.keys(this.dataset.label_info.detector_label_data);
    }
    this.experiment = {
      experiment_type: this.firstForm.value.typeOfExperiment,
      experiment_name: this.firstForm.value.name,
      model_type: this.modelName,
      lr: this.tuning.lrValue,
      image_size: this.tuning.imageSize,
      batch_size: this.tuning.batchSize,
      part_id: this.dataset._id,
      metrics: this.metrics,
      label_data:label_data,
      new_parts:this.tags,
    };
  }

  submit() {
    if(this.tags.length > 0){
      this.ref.close(this.experiment);
    }else{
      this.toastrService.danger('Please Enter IGBT Number');
      // alert("fill the value");
    }
  }
}
