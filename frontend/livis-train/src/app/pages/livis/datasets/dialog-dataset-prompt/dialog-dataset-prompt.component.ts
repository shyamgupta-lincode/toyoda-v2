import { Component, OnInit } from '@angular/core';
import { NbDialogRef } from '@nebular/theme';
import { FormGroup, FormBuilder, Validators } from '@angular/forms';

import { LivisService } from '../../livis.service';
import { NbToastrService } from '@nebular/theme';
@Component({
  selector: 'ngx-dialog-dataset-prompt',
  templateUrl: 'dialog-dataset-prompt.component.html',
  styleUrls: ['dialog-dataset-prompt.component.scss'],
  providers: [LivisService],
})
export class DialogDatasetPromptComponent implements OnInit {

  firstForm: FormGroup;
  secondForm: FormGroup;
  thirdForm: FormGroup;

  dataset: any = {};

  upload_id: string;
  isSubmitted = false;

  constructor(
    protected ref: NbDialogRef<DialogDatasetPromptComponent>,
    private fb: FormBuilder,
    private livisService: LivisService,
    private toastrService: NbToastrService,
  ) {}

  ngOnInit() {
    this.firstForm = this.fb.group({
      part_number: ['', Validators.required],
      part_description: ['', ],
    });

    this.secondForm = this.fb.group({
      datasetCtrl: ['', Validators.required],
      fileSource: ['', [Validators.required]],
    });
  }

  onFirstSubmit() {
    this.firstForm.markAsDirty();
  }

  onSecondSubmit() {
    this.secondForm.markAsDirty();
    const file = this.secondForm.get('fileSource').value;
    return this.livisService.upload_file(file);
  }

  onFileChange(event) {
    if (event.target.files.length > 0) {
      const file = event.target.files[0];
      this.secondForm.patchValue({
        fileSource: file,
      });
    }
  }

  cancel() {
    this.ref.close();
  }

  collectValues() {
    this.dataset = {
      part_number: this.firstForm.value.partNumberCtrl,
      line_number: this.firstForm.value.lineNumberCtrl,
      factory_code: this.firstForm.value.factoryCodeCtrl,
    };
  }

  submit() {
    this.isSubmitted = true;
    if(this.firstForm.valid)
    {
      // this.livisService.create_dataset
      // alert("success");
      this.isSubmitted = false;
      // console.log(this.firstForm.value);
      // this.livisService.create_dataset(this.firstForm.value)
      // .subscribe(data =>{
        // alert("success")
              // this.dataset.upload_id = data.;
      this.ref.close(this.firstForm.value);
      // this.ref.close();
        
        // this.toastrService.show(
        //   'This is super toast message',
        //   'top-right','success');
          // that.fetchDatasets();
        
        // this.alertService.alertMessage("Added Successfully","success","check");
      // });

// this.getModelList();
// this.loadAddForm();
// $("#add-part-modal").modal("hide");
       // this.onSecondSubmit().subscribe(data => {

    // });
    }
    // alert("hi");
    // this.firstForm.markAsDirty();
   
  }
}
