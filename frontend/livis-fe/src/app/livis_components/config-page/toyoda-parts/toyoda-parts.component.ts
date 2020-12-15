import { Component, OnInit, ViewChild,ViewEncapsulation } from '@angular/core';
import { MatSort} from '@angular/material/sort';
import {MatPaginator} from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';
import swal from 'sweetalert2';
import {FormBuilder, FormGroup, Validators } from '@angular/forms';
import {ToyodaPartService} from "../../../services/toyoda-part.service";
import {AlertService} from '../../../services/alert.service';

declare const $: any;

@Component({
  selector: 'app-toyoda-parts',
  templateUrl: './toyoda-parts.component.html',
  styleUrls: ['./toyoda-parts.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class ToyodaPartsComponent implements OnInit {
  availables:any;
  features:any;
  defects:any;
  partsForm: FormGroup;
  partsFormEdit: FormGroup;
  dataLength:number;
  isSubmitted = false;
  isSubmitedEdit = false;
  displayedColumns = ['sl', 'part_number','part_desc', 'operation'];
  dataSource:any;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort, {}) sort: MatSort;
  

  constructor(private _fb: FormBuilder,private toyodaPartService:ToyodaPartService,
    private alertService:AlertService) 
  { }

  ngAfterViewInit() {
  }
  ngOnInit(): void {
    this.loadAddForm();
    this.loadEditForm();
    this.getpartList();
    var model_info = {"features":["single_ringmark","brown","lotmark","arrow","model_no"],"model_no":"ca8" , "plugged_cell_percent": 2.5};
    this.availables = model_info.features;
    this.features = [];
    this.defects = [];

    // console.log(this.availables);
  }

  getpartList()
  {
    this.toyodaPartService.getParts()
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
      // short_number: ['', [Validators.required, ]],
      // model_number: ['', [Validators.required, ]],
      part_number: ['', [Validators.required]],
      // planned_production: ['', [Validators.required, ]],
      part_description:['', ],
      // edit_part_data:['', ],
      
    });
  }
  

  loadEditForm()
  {
    this.partsFormEdit = this._fb.group({
      _id: ['', [Validators.required]],
      // short_number: ['', [Validators.required, ]],
      // model_number: ['', [Validators.required, ]],
      part_number: ['', [Validators.required]],
      // planned_production: ['', [Validators.required, ]],
      part_description:['', ],
      // edit_part_data:['', ],
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
    // console.log(model.value);
    if(!this.partsForm.invalid){
      this.isSubmitted = false;
        this.toyodaPartService.addNewPart(model.value)
              .subscribe(data =>{
                this.alertService.alertMessage("Added Successfully","success","check");
                this.getpartList();
                this.loadAddForm();
                $("#add-part-modal").modal("hide");
        });
    
    }
  }

  editPart(id)
  {
    this.toyodaPartService.getPart(id)
      .subscribe(data =>{
        // console.log(data);

        this.partsFormEdit.patchValue({
          _id: data._id,
          // short_number:data.short_number,
          // model_number: data.model_number,
          part_number: data.part_number,
          part_description: data.part_description,

        });
        $("#edit-part-modal").modal("show");

    });
    
  }

  updatePartInfo(model)
  {
    // console.log(model.value);
    this.isSubmitedEdit = true;
    if(!this.partsFormEdit.invalid){
      this.isSubmitedEdit = false;
      this.toyodaPartService.updatePart(model.value)
            .subscribe(data =>{
              this.alertService.alertMessage("Updated Successfully","success","check");
              this.getpartList();
            $("#edit-part-modal").modal("hide");
      });
 
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
    this.toyodaPartService.deletePart(id)
            .subscribe(data =>{
              this.getpartList();
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




}
