import { Component, OnInit, ViewChild } from '@angular/core';
import { MatSort} from '@angular/material/sort';
import {MatPaginator} from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';
import swal from 'sweetalert2';
import {FormBuilder, FormGroup, Validators } from '@angular/forms';
import {ShiftService} from "../../../services/shift.service";
import {AlertService} from '../../../services/alert.service';
import * as moment from 'moment';


declare const $: any;


@Component({
  selector: 'app-shift',
  templateUrl: './shift.component.html',
  styleUrls: ['./shift.component.css']
})
export class ShiftComponent implements OnInit {
  
  time = {hour: 13, minute: 30};
  shiftForm: FormGroup;
  shiftFormEdit:FormGroup;
  isSubmitted = false;
  displayedColumns = ['sl','shift_name', 'start_time', 'end_time', 'status', 'operation'];
  dataSource: MatTableDataSource<any>;
  dataLength:number;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort, {}) sort: MatSort;
  constructor(private _fb: FormBuilder,private shiftService:ShiftService,
    private alertService:AlertService) 
  { }
    ngAfterViewInit() {
      // this.dataSource.paginator = this.paginator;
      // this.dataSource.sort = this.sort;
    }

    getShiftList()
    {
      this.shiftService.getShifts()
      .subscribe(data =>{
        this.dataSource = new MatTableDataSource(data);
        this.dataSource.data = data;
        this.dataLength = data.length;

        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
      });
    }
  
    ngOnInit() {
      this.loadAddForm();
      this.loadEditForm();
      this.getShiftList();
    }

    loadAddForm()
    {
      this.shiftForm = this._fb.group({
        shift_name: ['', [Validators.required, ]],
        start_time: ['', [Validators.required, ]],
        end_time: ['', [Validators.required, ]],
        status: [true, [Validators.required, ]],
      });
    }

    loadEditForm()
    {
      this.shiftFormEdit = this._fb.group({
        _id: ['', [Validators.required]],
        edit_shift_name: ['', [Validators.required]],
        edit_start_time: ['', [Validators.required, ]],
        edit_end_time: ['', [Validators.required, ]],
        edit_status: ['', ],
      });
    }
  
  
    filterShift(value: string):void{
      this.dataSource.filter = value.trim().toLowerCase();
    }

    addShift(element)
    {
      $("#add-shift-modal").modal("show");
      // console.log(element);
    }

    deleteShift(id)
    {
      swal({
        title: 'Are you sure?',
        text: 'You will not be able to recover this shift!',
        type: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, keep it',
        confirmButtonClass: "btn btn-success",
        cancelButtonClass: "btn btn-danger",
        buttonsStyling: false
    }).then((result) => {
      if (result.value) {
        this.shiftService.deleteShift(id)
        .subscribe(data =>{
          this.getShiftList();
          swal({
            title: 'Deleted!',
            text: 'Your shift info has been deleted.',
            type: 'success',
            confirmButtonClass: "btn btn-success",
            buttonsStyling: false
        }).catch(swal.noop)
        
        });
        
      } else {
        swal({
            title: 'Cancelled',
            text: 'Your shift info is safe :)',
            type: 'error',
            confirmButtonClass: "btn btn-info",
            buttonsStyling: false
        }).catch(swal.noop)
      }
    })
    }
  
    addNewShift(model)
    {
      this.isSubmitted = true;
      if(!this.shiftForm.invalid){
        
        var shiftInfo = model.value;
        shiftInfo.start_time = shiftInfo.start_time+":00";
        shiftInfo.end_time = shiftInfo.end_time+":00";
        // console.log(shiftInfo);
        this.shiftService.addShift(shiftInfo)
              .subscribe(data =>{
                this.alertService.alertMessage("Added Successfully","success","check");
                this.isSubmitted = false;
                this.getShiftList();
                this.loadAddForm();
                $("#add-shift-modal").modal("hide");
        });
       
      }
    }

    editShift(id)
    {
      this.shiftService.getShift(id)
              .subscribe(data =>{
                console.log(moment(data.start_time, "HH:mm:ss").format("HH:mm"));
                // console.log(moment(data.start_time).format("HH:mm"));
          this.shiftFormEdit.patchValue({
            _id: data._id,
            edit_shift_name: data.shift_name,
            edit_start_time: moment(data.start_time, "HH:mm:ss").format("HH:mm"),
            edit_end_time: moment(data.end_time, "HH:mm:ss").format("HH:mm"),
            edit_status: data.status,
          });
          $("#edit-shift-modal").modal("show");
      });
     

    }

    updateShift(model)
    {
      this.isSubmitted = true;
      if(!this.shiftFormEdit.invalid){
        var shiftInfo:any = {};
        shiftInfo._id = model.value._id;
        shiftInfo.shift_name = model.value.edit_shift_name;
        shiftInfo.status = model.value.edit_status;
        shiftInfo.start_time = model.value.edit_start_time+":00";
        shiftInfo.end_time = model.value.edit_end_time+":00";
        this.shiftService.updateShift(shiftInfo)
              .subscribe(data =>{
                this.alertService.alertMessage("Update Successfully","success","check");
                this.isSubmitted = false;
                this.getShiftList();
                $("#edit-shift-modal").modal("hide");
        });
      }
      // console.log(model.value);
    }

}
