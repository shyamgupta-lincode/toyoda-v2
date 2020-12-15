import { Component, OnInit, ViewChild,ViewEncapsulation } from '@angular/core';
import { MatSort} from '@angular/material/sort';
import {MatPaginator} from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';
import swal from 'sweetalert2';
import {FormBuilder, FormGroup, Validators } from '@angular/forms';
import {PmodelService} from "../../../services/pmodel.service";
import {AlertService} from '../../../services/alert.service';
import {CdkDragDrop, moveItemInArray, transferArrayItem} from '@angular/cdk/drag-drop';

declare const $: any;

@Component({
  selector: 'app-parts',
  templateUrl: './parts.component.html',
  styleUrls: ['./parts.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class PartsComponent implements OnInit {

  availables:any;
  features:any;
  defects:any;

  partsForm: FormGroup;
  partsFormEdit: FormGroup;
  dataLength:number;
  isSubmitted = false;
  isSubmitedEdit = false;

  displayedColumns = ['sl', 'model_number','part_number','bath_number', 'operation'];
//   test_data =  [{
//     id: 1,
//     model_number: 'Netgear Cable Modem',
//     part_number: 'CM700',
   
// },
// {
//     id: 2,
//     model_number: 'Linksys Cable Modem',
//     part_number: 'LK700',
// }];
  dataSource:any;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort, {}) sort: MatSort;
  

  constructor(private _fb: FormBuilder,private pmodelService:PmodelService,
    private alertService:AlertService) 
  { }
  
  ngAfterViewInit() {
    // console.log(this.paginator);
    // this.dataSource.paginator = this.paginator;
    // this.dataSource.sort = this.sort;
    // console.log(this.dataSource);
  }
  ngOnInit(): void {
    this.loadAddForm();
    this.loadEditForm();
    this.getModelList();
    var model_info = {"features":["single_ringmark","brown","lotmark","arrow","model_no"],"model_no":"ca8" , "plugged_cell_percent": 2.5};
    this.availables = model_info.features;
    this.features = [];
    this.defects = [];

    // console.log(this.availables);
  }
  getModelList()
  {
    this.pmodelService.getModels()
      .subscribe(data =>{
        this.dataSource = new MatTableDataSource(data);
        this.dataSource.data = data;
        this.dataLength = data.length;

        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
      });
    
  }
  loadAddForm()
  {
    this.partsForm = this._fb.group({
      part_number: ['', [Validators.required]],
      model: ['', [Validators.required, ]],
      bath_number_denominator: ['', [Validators.required, ]],
      plugged_cell_percent: ['', [Validators.required,Validators.pattern(/^\d+(\.\d+)*$/), ]],

    });
  }
  

  loadEditForm()
  {
    this.partsFormEdit = this._fb.group({
      _id: ['', [Validators.required]],
      edit_part_number: ['', [Validators.required]],
      edit_model: ['', [Validators.required, ]],
      edit_bath_number_denominator: ['', [Validators.required, ]],
    });
  }

  filterParts(value: string):void{
    this.dataSource.filter = value.trim().toLowerCase();
  }

  addParts()
  {
    $("#add-part-modal").modal("show");
  }

  addNewPart(model)
  {
    this.isSubmitted = true;
    if(!this.partsForm.invalid){
      console.log(this.features.length);
      if((this.features.length>0) && (this.defects.length>0)){
       
        model.value.availables = this.availables;
        model.value.features = this.features;
        model.value.defects = this.defects;
        // console.log(model.value);
        this.pmodelService.addModel(model.value)
              .subscribe(data =>{
                this.alertService.alertMessage("Added Successfully","success","check");
        });
        this.isSubmitted = false;
        this.getModelList();
        this.loadAddForm();
        $("#add-part-modal").modal("hide");
      }else{
        this.alertService.alertMessage("Atleast One feature and defect enable required","danger","close");
      }
    }
  }

  editPart(id)
  {
    this.pmodelService.getModel(id)
      .subscribe(data =>{
        // console.log(data);

        this.partsFormEdit.patchValue({
          _id: data._id,
          edit_model:data.model,
          edit_part_number: data.part_number,
          edit_bath_number_denominator: data.bath_number_denominator
        });
        $("#edit-part-modal").modal("show");

    });
    
  }

  updatePartInfo(model)
  {
    // console.log(model.value);
    this.isSubmitedEdit = true;
    if(!this.partsFormEdit.invalid){
      this.pmodelService.updateModel(model.value)
            .subscribe(data =>{
              this.alertService.alertMessage("Updated Successfully","success","check");
      });
      this.isSubmitedEdit = false;
      this.getModelList();
      $("#edit-part-modal").modal("hide");
    }
  }

deletePartInfo(id)
{
  swal({
    title: 'Are you sure?',
    text: 'You will not be able to recover this parts!',
    type: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, delete it!',
    cancelButtonText: 'No, keep it',
    confirmButtonClass: "btn btn-success",
    cancelButtonClass: "btn btn-danger",
    buttonsStyling: false
}).then((result) => {
  if (result.value) {
    this.pmodelService.deleteModel({_id:id})
            .subscribe(data =>{
              this.getModelList();
              swal({
                  title: 'Deleted!',
                  text: 'Your parts info has been deleted.',
                  type: 'success',
                  confirmButtonClass: "btn btn-success",
                  buttonsStyling: false
              }).catch(swal.noop)
            
    });
   
  } else {
    swal({
        title: 'Cancelled',
        text: 'Your parts info is safe :)',
        type: 'error',
        confirmButtonClass: "btn btn-info",
        buttonsStyling: false
    }).catch(swal.noop)
  }
})
}


drop(event: CdkDragDrop<string[]>) {
  console.log(this.availables); console.log(this.features); console.log(this.defects);
  if (event.previousContainer === event.container) {
    moveItemInArray(event.container.data, event.previousIndex, event.currentIndex);
  } else {
    transferArrayItem(event.previousContainer.data,
                      event.container.data,
                      event.previousIndex,
                      event.currentIndex);
  }
}

}
