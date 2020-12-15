import { Component, OnInit,ViewEncapsulation} from '@angular/core';
import {MatCheckboxModule} from "@angular/material/checkbox";
import {FormBuilder, FormGroup, Validators } from '@angular/forms';
import swal from 'sweetalert2';
import {ShiftService} from "../../../services/shift.service";
import {OperatorService} from '../../../services/operator.service';
import {PmodelService} from "../../../services/pmodel.service";
import {AlertService} from '../../../services/alert.service';
import { AuthenticationService } from '../../../services/authentication.service';
import { StorageService } from '../../../helpers/storage.service';
import { from } from 'rxjs';

declare const $: any;
@Component({
  selector: 'app-operator-page',
  templateUrl: './operator-page.component.html',
  styleUrls: ['./operator-page.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class OperatorPageComponent implements OnInit {
  shift_list:any;
  model_list:any;
  model_info:any;
  metrix_list:any ={};
  defect_list:any = {};
  current_process:any = {};
  bath_number_count = 4;
  // camera_urls = 4;
  checkBoxChecked = false;

  callback_seconds = 2000;

  process_id:any = "";
  // process_id:any = "";

  previous_process:any = {}

  process_summary:any = {}
  
  current_inception_id:any = null;

  constructor(private _fb: FormBuilder,
    private operatorService:OperatorService,
    private shiftService:ShiftService,
    private pmodelService:PmodelService,
    private authenticationService:AuthenticationService,
    private alertService:AlertService,
    private storageService:StorageService) 
    { }
  startProcessForm:FormGroup;
  endProcessForm:FormGroup;
  loginForm:FormGroup;
  updatePartForm:FormGroup;
  isSubmitted = false;
  isSubmittedEdit = false;
  user_unfo:any;
  camera_urls = ["../../../../assets/img/no-camera-live.png","../../../../assets/img/no-camera-live.png",
  "../../../../assets/img/no-camera-live.png","../../../../assets/img/no-camera-live.png"];
  defectListInterval:any;
  metrixListInterval:any;
  previousProcessChecked = false;

  cameraLayoutLoad()
  {
    var html = ``;
    
    var count_div = 4;
    var col_size = 6;
    var camera_list = this.camera_urls;
    for(var i =0;i<count_div;i++)
    {
      if((camera_list[i])){
        html += `<div style="padding-right:5px;padding-left:5px; height:${count_div<=2?'66vh':'33vh'}" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" >
        <img style="width:100%;height:100%" src="${camera_list[i]}" id="live_feed_${(i+1)}" alt="feed not available" >
          </div>`;
      }else{
        html += `<div style="padding-right:5px;padding-left:5px; height:${count_div<=2?'66vh':'33vh'}" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" >
        <img style="width:100%;height:100%" src="../../../../assets/img/no-camera-live.png" id="live_feed_${(i+1)}" alt="feed not available" >
          </div>`;
      }
    }
    $("#camera_layout_wrap").html(html);
  }
  ngDestroy()
  {
    if(this.defectListInterval){
      clearTimeout(this.defectListInterval);
    }
    if(this.metrixListInterval){
      clearTimeout(this.metrixListInterval);
    }
  }
  ngOnInit(): void {
    this.user_unfo = this.storageService.getUserDetails();
    this.loadStartForm();
    this.loadEndForm();
    this.loadLoginForm();
    this.loadPartForm();
    this.checkCurrentProcess();
    this.cameraLayoutLoad();
    this.shiftService.getShifts()
      .subscribe(data =>{
        this.shift_list = data;
    });
    this.pmodelService.getModels()
    .subscribe(data =>{
     this.model_list = data;
    });
    // this.alertDefects();  
  }
  checkCurrentProcess()
  {
    this.operatorService.checkProcess(this.user_unfo.workstation_id)
            .subscribe(data =>{
              // console.log(data.length);
              if(Object.keys(data).length !== 0 && data.constructor === Object && !data.finished){
               
                this.operatorService.getcameraFeed(this.user_unfo.workstation_id)
                .subscribe(feed_data =>{

                this.current_process = data;
                this.current_process._id = data._id;
                this.current_process.inception_id = data._id; 
                this.camera_urls = feed_data?feed_data:["","","","",""];
                this.bath_number_count = parseInt(data.bath_number_denominator);
                this.cameraLayoutLoad();
                
                $("#start_process_btn").addClass("invisible-element");
                $("#stop_process_btn").removeClass("invisible-element");
                var html = `<div class="row">
                  <div class="col-md-3 result-desc">
                    <span><b>Shift: </b>${data.shift.shift_name}</span>
                  </div>
                  <div class="col-md-3 result-desc">
                    <span><b>Model No: </b>${data.model}</span>
                  </div>
                  <div class="col-md-3 result-desc">
                    <span><b>Part No: </b>${data.part_number}</span>
                  </div>
                  <div class="col-md-3 result-desc">
                    <span><b>Lot No: </b>${data.lot_number}</span>
                  </div>
                </div>`;
                $("#start_data").html(html);
                $("#start-process-modal").modal("hide");
                this.getMetrix();
                this.getDefectList();      
              });
            }

              
    });
  }

  modelChange(model_id)
  {
    var model_data = {model:model_id}
    this.operatorService.getModelInfo(model_data)
    .subscribe(data =>{
      // console.log(data);
     this.model_info = data;
     this.startProcessForm.patchValue({
        part_number:data.part_number,
        bath_number_denominator: data.bath_number_denominator,
      });
    });
  }

  alertDefects()
  {
    $("#result-status-wrap").removeClass('card-header-success');
    $("#result-status-wrap").addClass('card-header-danger');
    $("#result-status").text("(REJECTED)");
    swal({
      title: "",
      html: "<h1 class='text-danger'>REJECTED</h1>",
      buttonsStyling: false,
      confirmButtonClass: "btn btn-danger",
      type: "error"
  }).catch(swal.noop);
    // swal({
    //   title: "",
    //   html: "<h1 class='text-danger'>REJECTED</h1>",
    //   timer: 2000,
    //   // customClass: 'defect-auto-alert-wrap',
    //   type: 'error',
    //   // width: '90vh',
    
    //   showConfirmButton: false
    // }).catch(swal.noop);
  }

  alertAccepted()
  {
    $("#result-status-wrap").removeClass('card-header-danger');
    $("#result-status-wrap").addClass('card-header-success');
    $("#result-status").text("(ACCEPTED)");

    swal({
      title: "",
      html: "<h1 class='text-success'>ACCEPTED</h1>",
      buttonsStyling: false,
      confirmButtonClass: "btn btn-success",
      type: "success"
  }).catch(swal.noop);
    // swal({
    //   title: "",
    //   html: "<h1 class='text-success'>ACCEPTED</h1>",
    //   timer: 2000,
    //   // customClass: 'defect-auto-alert-wrap',
    //   type: 'success',
    //   // width: '90vh',
    
    //   showConfirmButton: false
    // }).catch(swal.noop);
  }

  loadStartForm()
  {
    this.startProcessForm = this._fb.group({
      model: ['', [Validators.required, ]],
      part_number: ['', [Validators.required, ]],
      bath_number_denominator: ['', [Validators.required, ]],
      shift: ['', [Validators.required]],
      lot_number: ['', [Validators.required, ]],
      workstation_id: [this.user_unfo.workstation_id, [Validators.required, ]],
      user_id: [this.user_unfo.user_id, [Validators.required, ]],

    });
  }

  loadLoginForm()
  {
    this.loginForm = this._fb.group({
      email: ['', [Validators.required,Validators.email]],
      password: ['', [Validators.required]],
     
   });
  }

  loadPartForm()
  {
    this.updatePartForm = this._fb.group({
      _id: ['', [Validators.required]],
      part_number: ['', [Validators.required]],

   });
  }

  loadEndForm()
  {
    this.endProcessForm = this._fb.group({
      _id: [this.user_unfo.workstation_id, [Validators.required, ]],
      bathnum: ['', [Validators.required, ]],
    });
  }

  processStartForm()
  {
    // alert("hi");
    this.operatorService.previousProcess(this.user_unfo.workstation_id)
            .subscribe(data =>{
        this.previous_process = data;      
      $("#start-process-modal").modal("show"); 
    });

  }

  processEndForm()
  {
    // alert("hi");
    // console.log(this.current_process);
    this.endProcessForm.patchValue({
      _id:this.current_process._id,
    });
    $("#end-process-modal").modal("show");
  }
  startProcess(model)
  {
    console.log(model.value); 

    this.isSubmitted = true;
    if(!this.startProcessForm.invalid){
      this.operatorService.createProcess(model.value)
            .subscribe(data =>{
          this.isSubmitted = false;
              // console.log(model.value);
          this.current_process = model.value;
          this.current_process._id = data.id;
          this.current_process.inception_id = data.id; 
          this.camera_urls = data.feed_urls;
          this.bath_number_count = parseInt(model.value.bath_number_denominator);
          this.cameraLayoutLoad();
          
          $("#start_process_btn").addClass("invisible-element");
          $("#stop_process_btn").removeClass("invisible-element");
          var html = `<div class="row">
            <div class="col-md-3 result-desc">
              <span><b>Shift: </b>${data.data.shift.shift_name}</span>
            </div>
            <div class="col-md-3 result-desc">
              <span><b>Model No: </b>${model.value.model}</span>
            </div>
            <div class="col-md-3 result-desc">
              <span><b>Part No: </b>${model.value.part_number}</span>
            </div>
            <div class="col-md-3 result-desc">
              <span><b>Lot No: </b>${model.value.lot_number}</span>
            </div>
          </div>`;
          $("#start_data").html(html);
          $("#start-process-modal").modal("hide");
          this.getMetrix();
          this.getDefectList();
          this.alertService.alertMessage("Process Started","success","check");
          this.previousProcessChecked = false;
          // this.checkBoxChecked = false;
          $("#previsous-process-btn").prop("checked",false);
          $("#previsous-process-btn").removeClass('mat-checkbox-checked');
          ////static data for m
      }); 
    }
   
  

    
  }
  getMetrix()
  {
    // this.current_process.inception_id = "5ef48d9da16de63e8a575416"
    this.operatorService.getMetrix(this.current_process.inception_id)
      .subscribe(data =>{
        this.metrix_list = data;
    });
    this.metrixListInterval = setTimeout(()=> {
      this.getMetrix();
    }, 2000);
  }

  getDefectList()
  {
    // this.current_process.inception_id = "5ef48d9da16de63e8a575416";
    this.operatorService.getDefectList(this.current_process.inception_id)
      .subscribe(data =>{
        this.defect_list = {};
        // console.log(data.length);
        if(data.length > 0){
        //var defects = [{"_id": "5ef452b3cc5f4ca5a6fa2a1c", "ocr_result": "PA-6", "defect_list": ["Slurry Stick", "mantle dent"], "feature_list": ["model_no", "arrow"], "plugged_cell_percent": 0.6047531269807119, "serial_number": 9, "db_update_ready": true, "isAccepted": false, "missingFeatures": ["single_ringmark", "brown", "lotmark", "arrow", "model_no"]}];
          this.defect_list = data[0];
          this.defect_list.plugged_cell_percent = (parseFloat(this.defect_list.plugged_cell_percent)).toFixed(4);
          
          // this.current_inception_id = 1;
          if(!this.current_inception_id){
            // debugger;
            //this.current_inception_id = this.defect_list._id;
            this.current_inception_id = this.defect_list._id;
              if (!this.defect_list.isAccepted)
                this.alertDefects();
              if (this.defect_list.isAccepted)
                this.alertAccepted();  
          }
          else if(this.current_inception_id && (this.current_inception_id!=this.defect_list._id))
          {
            // debugger;
              this.current_inception_id = this.defect_list._id;
              if (!this.defect_list.isAccepted)
                this.alertDefects();
              if (this.defect_list.isAccepted)
                this.alertAccepted();    
          }
          else if (this.current_inception_id && (this.current_inception_id==this.defect_list._id)){
            //doconso
          }
        }
    });
   
    this.defectListInterval = setTimeout(()=> {
      this.getDefectList();
    }, 1000);
  }

  

  endProcess(model)
  {
    this.isSubmittedEdit = true;
    if(!model.invalid){
      this.isSubmittedEdit = false;
      this.operatorService.endProcess(model.value)
            .subscribe(data =>{
          $("#stop_process_btn").addClass("invisible-element");
          $("#start_process_btn").removeClass("invisible-element");
          var html = "";
          $("#start_data").html(html);
          $("#end-process-modal").modal("hide");
          // this.getProcessSummary();
          // this.addProcessSummarydata(this.process_summary);
          this.operatorService.getProcessSummary(this.current_process._id)
          .subscribe(data =>{
            // this.process_summary = data;
            this.addProcessSummarydata(data);
            this.loadStartForm();
            this.loadEndForm();

            this.current_process = {};
            this.camera_urls = ["","","",""];
            this.cameraLayoutLoad();
            $("#process-summary-modal").modal("show");
            if(this.defectListInterval){
              clearTimeout(this.defectListInterval);
            }
            if(this.metrixListInterval){
              clearTimeout(this.metrixListInterval);
            }
          });
          

      });

    }
  }

  counterBathNumber(i: number) {
    // console.log(i);
    return new Array(i);
  }

  checkPreviosProcess(elem)
  {
    if(elem.checked){
      console.log(this.previous_process);
      
      this.startProcessForm.patchValue({
        shift:this.previous_process.shift._id,
        model:this.previous_process.model,
        part_number:this.previous_process.part_number,
        bath_number_denominator:this.previous_process.bath_number_denominator,
        lot_number:this.previous_process.lot_number,
      });
    }else{
      this.startProcessForm.patchValue({
        shift:"",
        model:"",
        part_number:"",
        bath_number_denominator:"",
        lot_number:"",
      });
    }
    // console.log(elem.checked);
  }

  editPartNumber()
  {
    $("#part-auth-modal").modal("show");
  }

  addProcessSummarydata(data)
  {
    var html =  `
    <div class="process-summary-wrap">
        <div class="row">
          <div class="card">
          
          <div class="card-body">
            <div class="row">
              <div class="col-md-1">
                <div class="operator-img">
                    <img src="./assets/img/faces/marc.jpg" />
                </div>
            
              </span>
              </div>
              <div class="col-md-10">
                <span><b>Name: </b>${this.user_unfo.name?this.user_unfo.name:"--"}<span>
                <br>
                <span><b>Role: </b>${this.user_unfo.role?this.user_unfo.role:"--"}<span>
              </div>
            </div>
          </div>
        </div>
        </div>

        <div class="row">

          <div class="col-md-4">
            <div class="card">
              <div class="card-body">
                  <div class="process-text-wrap text-center">
                    <span class="summary-heading">Total Scan</span>
                    <p class="summary-data">${data.total_parts?data.total_parts:"0"}</p>
                  </div>
              </div> 
            </div>  
          </div>

          <div class="col-md-4">
            <div class="card">
              <div class="card-body">
                  <div class="process-text-wrap text-center">
                    <span class="summary-heading">Accepted</span>
                    <p class="summary-data">${data.total_accepted_parts?data.total_accepted_parts:"0"}</p>
                  </div>
              </div> 
            </div>  
          </div>

          <div class="col-md-4">
            <div class="card">
              <div class="card-body">
                  <div class="process-text-wrap text-center">
                    <span class="summary-heading">Rejected</span>
                    <p class="summary-data">${data.total_rejected_parts?data.total_rejected_parts:"0"}</p>
                  </div>
              </div> 
            </div>  
          </div>

        </div>    
        
        <div class="row">

          <div class="col-md-3">
            <div class="card">
              <div class="card-body">
                  <div class="process-text-wrap text-center">
                    <span class="summary-heading">Shift</span>
                    <p class="summary-data">${data.shift?data.shift.shift_name:"--"}</p>
                  </div>
              </div> 
            </div>  
          </div>

          <div class="col-md-3">
            <div class="card">
              <div class="card-body">
                  <div class="process-text-wrap text-center">
                    <span class="summary-heading">Start Time</span>
                    <p class="summary-data">${data.shift?data.shift.start_time:"--"}</p>
                  </div>
              </div> 
            </div>  
          </div>

          <div class="col-md-3">
            <div class="card">
              <div class="card-body">
                  <div class="process-text-wrap text-center">
                    <span class="summary-heading">End Time</span>
                    <p class="summary-data">${data.shift?data.shift.end_time:"--"}</p>
                  </div>
              </div> 
            </div>  
          </div>
          <div class="col-md-3">
            <div class="card">
              <div class="card-body">
                  <div class="process-text-wrap text-center">
                    <span class="summary-heading">Working Time</span>
                    <p class="summary-data">${data.duration?data.duration:"--"}</p>
                  </div>
              </div> 
            </div>  
          </div>

        </div>    

        <div class="row">

        <div class="col-md-3">
          <div class="card">
            <div class="card-body">
                <div class="process-text-wrap text-center">
                  <span class="summary-heading">Model No.</span>
                  <p class="summary-data">${data.model?data.model:"--"}</p>
                </div>
            </div> 
          </div>  
        </div>

        <div class="col-md-3">
          <div class="card">
            <div class="card-body">
                <div class="process-text-wrap text-center">
                  <span class="summary-heading">Part No.</span>
                  <p class="summary-data">${data.part_number?data.part_number:"--"}</p>
                </div>
            </div> 
          </div>  
        </div>

        <div class="col-md-3">
          <div class="card">
            <div class="card-body">
                <div class="process-text-wrap text-center">
                  <span class="summary-heading">Lot No.</span>
                  <p class="summary-data">${data.lot_number?data.lot_number:"--"}</p>
                </div>
            </div> 
          </div>  
        </div>
        <div class="col-md-3">
          <div class="card">
            <div class="card-body">
                <div class="process-text-wrap text-center">
                  <span class="summary-heading">Bath No.</span>
                  <p class="summary-data">${data.bathnum?data.bathnum:"--"}</p>
                </div>
            </div> 
          </div>  
        </div>

      </div>    




    </div>    
    `;
    $("#process_data").html(html);
  }

  partAuthLogin(model)
  {
    this.isSubmitted = true;
    if(!model.invalid){
      this.isSubmitted = false;
      this.authenticationService.userLogin(model.value.email,model.value.password,this.user_unfo.workstation_id)
        .subscribe(data =>{
          this.updatePartForm.patchValue({
            _id:"1",
            part_number:$("#livis-part-number").text(),
          });
          $("#part-auth-modal").modal("hide");
          $("#edit-part-modal").modal("show");
      });
    
      
      
    }
  }

  updatePartInfo(model)
  {
    this.isSubmitted = true;
    if(model.valid){
        var ocr_info = {inspection_id:this.current_process._id,current_inspected_part_id:this.defect_list._id,ocr_result:model.value.part_number};
        // this.defect_list.ocr_result = model.value.part_number;
        this.operatorService.updateOcr(ocr_info)
        .subscribe(data =>{
          this.defect_list.ocr_result = model.value.part_number;
          $("#edit-part-modal").modal("hide");
          this.alertService.alertMessage("Model Number Updated","success","check");
        });
    }else{
      console.log(model.value);
    }
  }

  imageExists(image_url):any{

    $.get(image_url)
    .done(function() { 
       return true;
    }).fail(function() { 
        return false;

    })

  }

  getProcessSummary()
  {
    this.operatorService.getProcessSummary(this.current_process._id)
    .subscribe(data =>{
      this.process_summary = data;
    });
  }
  



}
