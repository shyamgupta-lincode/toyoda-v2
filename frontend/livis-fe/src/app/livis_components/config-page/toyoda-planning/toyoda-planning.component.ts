import { Component, OnInit, ViewChild,ViewEncapsulation } from '@angular/core';
import { MatSort} from '@angular/material/sort';
import {MatPaginator} from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';
import swal from 'sweetalert2';
import {FormBuilder, FormGroup, Validators } from '@angular/forms';
import {PmodelService} from "../../../services/pmodel.service";
import {ToyodaPlanningService} from "../../../services/toyoda-planning.service";
import {ToyodaPartService} from "../../../services/toyoda-part.service";


import {AlertService} from '../../../services/alert.service';
import * as moment from 'moment';

declare const $: any;

@Component({
  selector: 'app-toyoda-planning',
  templateUrl: './toyoda-planning.component.html',
  styleUrls: ['./toyoda-planning.component.css']
})
export class ToyodaPlanningComponent implements OnInit {

  part_list:any;
  features:any;
  defects:any;
  planForm: FormGroup;
  planFormEdit: FormGroup;
  dataLength:number;
  isSubmitted = false;
  isSubmitedEdit = false;
  displayedColumns = ['sl', 'part_number','start_date','end_date','short_number','planned_production', 'operation'];
  dataSource:any;
  current_date:any; 
  editDateRange:any;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort, {}) sort: MatSort;
  

  constructor(private _fb: FormBuilder,private pmodelService:PmodelService,
    private alertService:AlertService,
    private toyodaPlanningService:ToyodaPlanningService,
    private toyodaPartService:ToyodaPartService) 
  { }


  ngAfterViewInit() {
  }
  ngOnInit(): void {
    this.loadAddForm();
    this.loadEditForm();
    this.getPlanningList();
    this.getPartList();
    this.current_date = (moment().format("YYYY-MM-DD HH:mm:ss"));
  }

  getPartList()
  {
    this.toyodaPartService.getParts()
      .subscribe(data =>{
        this.part_list = data;
    })
  }

  getPlanningList()
  {
    this.toyodaPlanningService.getPlannings()
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
    this.planForm = this._fb.group({
      date_range: ['', [Validators.required, ]],
      part_number: ['', [Validators.required, ]],
      short_number: ['', [Validators.required]],
      planned_production_count: ['', [Validators.required, ]],
      // short_number_sel: ['', [Validators.required, ]],
    });
  }
  

  loadEditForm()
  {
    this.planFormEdit = this._fb.group({
      _id: ['', [Validators.required]],
      date_range: ['', [Validators.required, ]],
      part_number: ['', [Validators.required, ]],
      short_number: ['', [Validators.required]],
      planned_production_count: ['', [Validators.required, ]],
      // short_number_sel: ['', [Validators.required, ]],
    });
  }

  filterParts(value: string):void{
    this.dataSource.filter = value.trim().toLowerCase();
  }

  addParts()
  {
    $("#add-part-modal").modal("show");
  }

  addNewPlan(model)
  {
    this.isSubmitted = true;
    console.log(model.value);
    if(!this.planForm.invalid){
        // console.log(model.value);
        this.isSubmitted = false;
        model.value.start_time = model.value.date_range.start.format("YYYY-MM-DD");
        model.value.end_time = model.value.date_range.end.format("YYYY-MM-DD");

        this.toyodaPlanningService.addPlan(model.value)
              .subscribe(data =>{
                this.getPlanningList();
                this.loadAddForm();
                $("#add-part-modal").modal("hide");
                this.alertService.alertMessage("PlanAdded Successfully","success","check");
        });
    
    }else{
      console.log("validation error")
    }
  }

  editPlan(id)
  {
    this.toyodaPlanningService.getPlanning(id)
      .subscribe(data =>{
        // console.log(data);
        this.editDateRange = {start: data.start_time, end: data.end_time}
        this.planFormEdit.patchValue({
          _id: data._id,
          // date_range:"2000-01-01 - 2002-01-02",
          part_number: data.part_number,
          short_number: data.short_number,
          planned_production_count: data.planned_production_count,
          // short_number_sel: data.short_number_sel,

        });
        $("#edit-plan-modal").modal("show");

    });
    
  }

  updatePlan(model)
  {
    // console.log(model.value);
    this.isSubmitedEdit = true;
    if(!this.planFormEdit.invalid){
      this.isSubmitedEdit = false;
      model.value.start_time = model.value.date_range.start.format("YYYY-MM-DD");
      model.value.end_time = model.value.date_range.end.format("YYYY-MM-DD");

      this.toyodaPlanningService.updatePlan(model.value)
            .subscribe(data =>{
              this.alertService.alertMessage("Updated Successfully","success","check");
              this.getPlanningList();
              $("#edit-plan-modal").modal("hide");
      });
      
     
    }
  }

deletePlanInfo(id)
{
  swal({
    title: 'Are you sure?',
    text: 'You will not be able to recover this plans!',
    type: 'warning',
    showCancelButton: true,
    confirmButtonText: 'Yes, delete it!',
    cancelButtonText: 'No, keep it',
    confirmButtonClass: "btn btn-success",
    cancelButtonClass: "btn btn-danger",
    buttonsStyling: false
}).then((result) => {
  if (result.value) {
    this.toyodaPlanningService.deletePlanning(id)
            .subscribe(data =>{
              this.getPlanningList();
              swal({
                  title: 'Deleted!',
                  text: 'Your plan info has been deleted.',
                  type: 'success',
                  confirmButtonClass: "btn btn-success",
                  buttonsStyling: false
              }).catch(swal.noop)
            
    });
   
  } else {
    swal({
        title: 'Cancelled',
        text: 'Your plan info is safe :)',
        type: 'error',
        confirmButtonClass: "btn btn-info",
        buttonsStyling: false
    }).catch(swal.noop)
  }
})
}

partChange(id)
  {
    this.toyodaPartService.getPartByShortNumber(id)
      .subscribe(data =>{
        this.planForm.patchValue({
          part_number: data.part_number,
          short_number: data.short_number,
        });
    })
  }

  transferToDate(input)
  {
      return  moment(input, "YYYY-MM-DD HH:mm:ss").format("YYYY-MM-DD");
  }


}
