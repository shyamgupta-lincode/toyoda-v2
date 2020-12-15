import { Component, OnInit,ViewEncapsulation} from '@angular/core';
import {MatCheckboxModule} from "@angular/material/checkbox";
import {FormBuilder, FormGroup, Validators } from '@angular/forms';
import swal from 'sweetalert2';
import {ShiftService} from "../../../services/shift.service";
import {ToyodaOperatorService} from '../../../services/toyoda-operator.service';
import {ToyodaPartService} from "../../../services/toyoda-part.service";
import {AlertService} from '../../../services/alert.service';
import { AuthenticationService } from '../../../services/authentication.service';
import { StorageService } from '../../../helpers/storage.service';
import { from } from 'rxjs';
import { analyzeAndValidateNgModules } from '@angular/compiler';

declare const $: any;

@Component({
  selector: 'app-toyoda-operator',
  templateUrl: './toyoda-operator.component.html',
  styleUrls: ['./toyoda-operator.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class ToyodaOperatorComponent implements OnInit {

  user_info:any;
  camera_urls:any = [""];
  loginForm:FormGroup;
  inspectionQcForm:FormGroup;
  pdnCounterForm:FormGroup;
  processStartForm:FormGroup;
  rescanForm:FormGroup;
  isSubmitted:any=false;
  part_list = [];
  current_process:any = {}
  metrix_list:any = {};
  defect_list:any = {};
  current_inception_id:any = null;
  defectListInterval:any;
  metrixListInterval:any;
  runningProcessInterval:any;

  process_summary:any = {};
  production_counter:any; 
  inspection_count = 0;
  cancel_text:any = "Cancel";

  reached_status_alert = false;
  constructor(private _fb: FormBuilder,
    private toyodaOperatorService:ToyodaOperatorService,
    private shiftService:ShiftService,
    private toyodaPartService:ToyodaPartService,
    private authenticationService:AuthenticationService,
    private alertService:AlertService,
    private storageService:StorageService) 
    { }
  

  ngOnInit(): void {
    // window.location.href;
    this.user_info = this.storageService.getUserDetails();
    this.loadLoginForm();
    this.loadQcForm();
    this.loadProdCounterForm();
    this.loadProcessStartForm();
    this.loadRescanForm();
    this.cameraLayoutLoad();
    this.getPartList();
    this.getRunningProcess();
    // this.inspectionAlert();
    // this.alertDefects();
    // this.limitAlert();
    // this.getProcessSummary();
    // this.processEndedAlert();
    // this.getDefectList();
  }

  ngOnDestroy() {
    if(this.runningProcessInterval)
    {
      clearTimeout(this.runningProcessInterval);
    }
    if(this.defectListInterval)
    {
      clearTimeout(this.defectListInterval);
    }
    if(this.metrixListInterval)
    {
      clearTimeout(this.metrixListInterval);
    }
    // console.log('Items destroyed');
    // alert("I am in destroy mode");
  }

  getProcessSummary()
  {
    // console.log(this.current_process);
    this.toyodaOperatorService.getProcessSummary(this.current_process._id)
      .subscribe(data =>{
        this.current_process = {};
        this.process_summary = data;
        $("#process-summary-modal").modal("show");
    });
    
  }

  alertDefects()
  {
    $("#result-status-wrap").removeClass('card-header-success');
    $("#result-status-wrap").removeClass('card-header-livis-gray');
    $("#result-status-wrap").addClass('card-header-danger');

    $("#streaming-camera-wrap").removeClass('card-header-success');
    $("#streaming-camera-wrap").removeClass('card-header-livis-gray');
    $("#streaming-camera-wrap").addClass('card-header-danger');
    $("#result-status").text("(NG)");
    swal({
      title: "",
      html: "<h1 class='text-danger'>NG</h1>",
      buttonsStyling: false,
      confirmButtonClass: "btn btn-danger",
      type: "error"
  }).catch(swal.noop);
  }

  alertAccepted()
  {
    $("#result-status-wrap").removeClass('card-header-danger');
    $("#result-status-wrap").removeClass('card-header-livis-gray');
    $("#result-status-wrap").addClass('card-header-success');

    $("#streaming-camera-wrap").removeClass('card-header-danger');
    $("#streaming-camera-wrap").removeClass('card-header-livis-gray');
    $("#streaming-camera-wrap").addClass('card-header-success');

    $("#result-status").text("(OK)");

    swal({
      title: "",
      html: "<h1 class='text-success'>OK</h1>",
      timer: 2000,
      // customClass: 'defect-auto-alert-wrap',
      type: 'success',
      // width: '90vh',
    
      showConfirmButton: false
    }).catch(swal.noop);

  //   swal({
  //     title: "",
  //     html: "<h1 class='text-success'>OK</h1>",
  //     buttonsStyling: false,
  //     confirmButtonClass: "btn btn-success",
  //     type: "success"
  // }).catch(swal.noop);
  }

  processEndedAlert()
  {
    this.current_process = {};
    this.defect_list = {};
    this.metrix_list = {};
    if(this.runningProcessInterval)
    {
      clearTimeout(this.runningProcessInterval);
    }
    if(this.defectListInterval)
    {
      clearTimeout(this.defectListInterval);
    }
    if(this.metrixListInterval)
    {
      clearTimeout(this.metrixListInterval);
    }
    swal({
      title: "",
      html: "<h1 class='text-success'>Process End</h1>",
      buttonsStyling: false,
      confirmButtonClass: "btn btn-success",
      type: "success"
  }).catch(swal.noop);
  }

  getMetrix()
  {
    // this.current_process.inception_id = "5ef48d9da16de63e8a575416"
    this.toyodaOperatorService.getMetrix(this.current_process._id)
      .subscribe(data =>{
        
        if(data.qc_inspection.length > 0)
        {
          this.inspection_count = data.qc_inspection.length;
         
          
          if(data.qc_inspection.length == 3)
          {
            $("#start_process_btn").addClass("invisible-element");
            $("#stop_process_btn").removeClass("invisible-element");
          }

        }

        // console.log(data.accepted);
        // console.log(this.production_counter);


        if(data.accepted > 0 && (data.accepted == this.production_counter) && !this.reached_status_alert)
        {
          this.reached_status_alert = true;
          if(this.inspection_count == 3)
          {
            this.limitAlert();
          }else{
            this.inspectionAlert();
          }
        }    
        // console.log(this.inspection_count);
        this.metrix_list = data;
    });
    this.metrixListInterval = setTimeout(()=> {
      this.getMetrix();
    }, 2000);
  }

  getDefectList()
  {
    // this.current_process.inception_id = "5f36381b493087e4203d2d1c";
    // console.log(this.current_process._id)
    this.toyodaOperatorService.getDefectList(this.current_process._id)
      .subscribe(data =>{
        // console.log(data);
        this.defect_list = {};
        if(Object.keys(data).length !== 0 && data.constructor === Object ){
        //var defects = [{"_id": "5ef452b3cc5f4ca5a6fa2a1c", "ocr_result": "PA-6", "defect_list": ["Slurry Stick", "mantle dent"], "feature_list": ["model_no", "arrow"], "plugged_cell_percent": 0.6047531269807119, "serial_number": 9, "db_update_ready": true, "isAccepted": false, "missingFeatures": ["single_ringmark", "brown", "lotmark", "arrow", "model_no"]}];
          this.defect_list = data;
          // console.log(this.defect_list);
          // this.defect_list.plugged_cell_percent = (parseFloat(this.defect_list.plugged_cell_percent)).toFixed(4);
          
          // this.current_inception_id = 1;
          if(!this.current_inception_id){
            // debugger;
            //this.current_inception_id = this.defect_list._id;
            this.current_inception_id = this.defect_list._id;
              if (!this.defect_list.isAccepted)
                this.alertDefects();
              if (this.defect_list.isAccepted)
                this.alertAccepted();  
            // if(this.metrix_list.accepted > 0 && (this.metrix_list.accepted == this.production_counter))
            // {
            //   if(this.inspection_count == 3)
            //   {
            //     this.limitAlert();
            //   }else{
            //     this.inspectionAlert();
            //   }
            // }    
          }
          else if(this.current_inception_id && (this.current_inception_id!=this.defect_list._id))
          {
            // debugger;
              this.current_inception_id = this.defect_list._id;
              if (!this.defect_list.isAccepted)
                this.alertDefects();
              if (this.defect_list.isAccepted)
                this.alertAccepted();   
              // if(this.metrix_list.accepted > 0 && (this.metrix_list.accepted == this.production_counter))
              // {
              //   if(this.inspection_count == 3)
              //   {
              //     this.limitAlert();
              //   }else{
              //     this.inspectionAlert();
              //   }
              // }       
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

  getPartList()
  {
    this.toyodaPartService.getParts()
      .subscribe(data =>{
        this.part_list = data;
    })
  }

  getCameraFeedUrl()
  {
    this.toyodaOperatorService.getCameraFeed(this.user_info.workstation_id)
      .subscribe(data =>{
        this.camera_urls = data;
        this.cameraLayoutLoad();
    })
  }
  getRunningProcess()
  {
    this.toyodaOperatorService.getRunningProcess(this.user_info.workstation_id)
    .subscribe(data =>{
      if(Object.keys(data).length !== 0 && data.constructor === Object ){
        if(!this.current_process._id)
        {
          this.current_process = data;
          this.getCameraFeedUrl();
          this.getDefectList();
          this.getMetrix();
          
          if(!this.production_counter){
            this.production_counter = data.plan?data.plan.planned_production_count:0;
          }
          // alert("dd");
          $("#start_process_btn").addClass("invisible-element");
          $("#stop_process_btn").removeClass("invisible-element");
        }
      }else{
        if(this.current_process._id)
        {
         

          this.processEndedAlert();
        }
      }
      // console.log(data);
    })

    // this.runningProcessInterval = setTimeout(()=> {
    //   this.getRunningProcess();
    // }, 1000);
  }

  startProcess(model)
  {
    this.isSubmitted = true;
    if(!this.processStartForm.invalid){
      this.isSubmitted = false;
      this.toyodaOperatorService.startProcess(model.value)
            .subscribe(data =>{
              this.alertService.alertMessage("Process Started Successfully","success","check");
              this.current_process = data; 
              this.loadProcessStartForm();
              this.getCameraFeedUrl();
              
              this.getDefectList();
              this.getMetrix();
              if(this.runningProcessInterval){
                clearTimeout(this.runningProcessInterval);
              }
              $("#start_process_btn").addClass("invisible-element");
              $("#stop_process_btn").removeClass("invisible-element");
              $("#process-start-modal").modal("hide");
      });
 
    }else{
      // console.log(model.value);
    }
  }

processEndForm()
{
    swal({
      title: '',
      text: 'Are you sure you want to end process',
      type: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Ok',
      cancelButtonText: 'Cancel',
      confirmButtonClass: "btn btn-success",
      cancelButtonClass: "btn btn-danger",
      buttonsStyling: false
  }).then((result) => {
    if(1)
    {
      if (result.value) {
        var end_info = {process_id:this.current_process._id};
        this.toyodaOperatorService.endProcess(end_info)
              .subscribe(data =>{
            $("#stop_process_btn").addClass("invisible-element");
            $("#start_process_btn").removeClass("invisible-element");
            
            if(this.defectListInterval){
              this.defect_list = {};
              clearTimeout(this.defectListInterval);
            }
            if(this.metrixListInterval){
              this.metrix_list = {};
              clearTimeout(this.metrixListInterval);
            }
            if(this.runningProcessInterval)
            {
              clearTimeout(this.metrixListInterval);
            }
           
          this.alertService.alertMessage("Process Ended Successfully","success","check");
          // this.processEndedAlert();
          // this.getProcessSummary();      
        });
      
      } 
    }else{
      this.quantityAlert();
    }    
   
  })
}

  cameraLayoutLoad()
  {
    var html = ``;
    
    var count_div = 1;
    var col_size = 12;
    var camera_list = this.camera_urls;
    // for(var i =0;i<count_div;i++)
    // {
      if((camera_list['top'] != false)){
        html += `<div style="padding-right:5px;padding-left:5px; height:${count_div<=2?'64vh':'32vh'}" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" >
        <img style="width:100%;height:100%" src="${camera_list['top']}" id="live_feed_${(1)}" alt="feed not available" >
          </div>`;
      }else{
        html += `<div style="padding-right:5px;padding-left:5px; height:${count_div<=2?'64vh':'32vh'}" class="col-lg-${col_size} col-md-${col_size} col-sm-${col_size} camera-img-wrap" >
        <img style="width:100%;height:100%" src="../../../../assets/img/no-camera-live.png" id="live_feed_${(1)}" alt="feed not available" >
          </div>`;
      }
    // }
    $("#camera_layout_wrap").html(html);
  }

  loadLoginForm()
  {
    this.loginForm = this._fb.group({
      email: ['', [Validators.required,Validators.email]],
      password: ['', [Validators.required]],
      fn_type: ['', [Validators.required]],
      inspection_type: ['', ],

   });
  }

  loadQcForm()
  {
    this.inspectionQcForm = this._fb.group({
      qc_status: ['1', [Validators.required]],
      // part_weight: ['', [Validators.required]],
      qc_remark: ['', [Validators.required]],
      inspection_type: ['', [Validators.required]],
      process_id: ['', [Validators.required]],
   });
  }

  loadProdCounterForm()
  {
    this.pdnCounterForm = this._fb.group({
      process_id: ['', [Validators.required]],
      planned_production: ['', [Validators.required]],
   });
  }

  loadProcessStartForm()
  {
    this.processStartForm = this._fb.group({
      workstation_id: ['', [Validators.required]],
      user_id: ['', [Validators.required]],
      part_number: ['', [Validators.required]],
      // model_number: ['', [Validators.required]],
      // short_number: ['', [Validators.required]],
      part_description: ['', ],
   });
  }

  loadRescanForm()
  {
    this.rescanForm = this._fb.group({
      process_id: ['', [Validators.required]],
      inspection_id: ['', [Validators.required]],
      part_number: ['', [Validators.required]],
      model_number: ['', [Validators.required]],
      short_number: ['', [Validators.required]],
      part_description: ['', ],
      rescan_status: ['1', ],

      
   });
  }

  loadAuthModel(type,inspection_type="")
  {
    this.loginForm.patchValue({
      fn_type: type,
      inspection_type:inspection_type
    });
      $("#user-auth-modal").modal("show");
    // $("#inspection-qc-modal").modal("show");
    // $("#planned-production-modal").modal("show");
   
  }

  authLogin(model)
  {
    // console.log(model.value);
    this.isSubmitted = true;
    if(!model.invalid){
      this.isSubmitted = false;
      this.authenticationService.checkUserLogin(model.value.email,model.value.password,this.user_info.workstation_id)
        .subscribe(data =>{
          var login_info:any = data;
          if(login_info.role_name == "supervisor"){
            $("#user-auth-modal").modal("hide");
            if(model.value.fn_type === "inspection_qc")
            {
              this.inspectionQcForm.patchValue({
                inspection_type:model.value.inspection_type,
                process_id:this.current_process._id,
              });
              $("#inspection-qc-modal").modal("show");
            }else if(model.value.fn_type === "production_counter")
            {
              this.pdnCounterForm.patchValue({
                process_id:this.current_process._id,
                planned_production:this.production_counter,
              });
              $("#planned-production-modal").modal("show");
            }
          }else{
            this.alertService.alertMessage("Only Superviser Can Access","danger","close");
          }
          // // this.updatePartForm.patchValue({
          // //   _id:"1",
          // //   part_number:$("#livis-part-number").text(),
          // // });
          // $("#part-auth-modal").modal("hide");
          // $("#edit-part-modal").modal("show");
      });
    
      
      
    }
  }

  addInspectionStatus(model)
  {
    this.isSubmitted = true;
    if(!model.invalid){
      this.isSubmitted = false;
      this.toyodaOperatorService.updateInspectionQc(model.value)
            .subscribe(data =>{
              this.alertService.alertMessage("QC record Successfully","success","check");
            this.loadQcForm();  
            $("#inspection-qc-modal").modal("hide");
      });
    }else{
      // console.log(model.value);
      // console.log("Validation Error")
    }
  }

  updatePlannedProduction(model)
  {
    this.isSubmitted = true;
    if(!model.invalid){
      this.isSubmitted = false;
      var production_info:any = {};
      production_info.process_id = model.value.process_id;
      production_info.current_production_count = model.value.planned_production;

      this.toyodaOperatorService.modifyPlannedProduction(production_info)
            .subscribe(data =>{
             this.production_counter =  production_info.current_production_count;
              this.alertService.alertMessage("QC record Successfully","success","check");
            $("#inspection-qc-modal").modal("hide");
      });
    }else{
      // console.log(model.value);
      // console.log("Validation Error")
    }
  }

  showStartForm()
  {
    this.getPartList();
    $("#process-start-modal").modal("show");
  }
  partChange(id)
  {
    this.toyodaPartService.getPart(id)
      .subscribe(data =>{
        this.production_counter = data.planned_production;
        this.processStartForm.patchValue({
          // model_number: data.model_number,
          // part_number: data.part_number,
          part_description: data.part_description,
          workstation_id:this.user_info.workstation_id,
          user_id:this.user_info.user_id,
        });
    })
  }

limitAlert()
{
  swal({
    title: '',
    text: 'Planned Production Achieved',
    type: 'success',
    showCancelButton: true,
    confirmButtonText: 'Add & Resume',
    cancelButtonText: this.cancel_text,
    confirmButtonClass: "btn btn-success",
    cancelButtonClass: "btn btn-danger",
    buttonsStyling: false
}).then((result) => {
  if (result.value) {
    this.loadAuthModel('production_counter');
  } else {

    var end_info = {process_id:this.current_process._id};
    this.toyodaOperatorService.endProcess(end_info)
          .subscribe(data =>{
        $("#stop_process_btn").addClass("invisible-element");
        $("#start_process_btn").removeClass("invisible-element");
        
        if(this.defectListInterval){
          this.defect_list = {};
          clearTimeout(this.defectListInterval);
        }
        if(this.metrixListInterval){
          this.metrix_list = {};
          clearTimeout(this.metrixListInterval);
        }
        if(this.runningProcessInterval)
        {
          clearTimeout(this.metrixListInterval);
        }
        
      this.alertService.alertMessage("Process End Successfully","success","check");
      this.getProcessSummary();      
    });
    // this.processEndedAlert();
  }
})
}

inspectionAlert()
{
  swal({
    title: "Inspection QC",
    html: "<h4 class='text-danger'>Please complete Inspection QC to end the process</h4>",
    buttonsStyling: false,
    confirmButtonClass: "btn btn-danger",
    type: "error"
}).catch(swal.noop);
}

quantityAlert()
{
  swal({
    title: "Quantity Alert",
    html: "<h4 class='text-danger'>Planned production not achieved.You cant end the process</h4>",
    buttonsStyling: false,
    confirmButtonClass: "btn btn-danger",
    type: "error"
}).catch(swal.noop);
}

showRescanModel()
{
  this.rescanForm.patchValue({
    process_id: this.current_process._id,
    inspection_id: this.current_process._id,
    part_number: '2222',
    model_number: '111',
    short_number: '111',
    part_description: 'tset',
 });
  $("#rescan-part-modal").modal("show");
}

updateRescan(model)
{
  this.isSubmitted = true;
  if(!model.invalid){
    this.isSubmitted = false;
    this.toyodaOperatorService.rescanProcess(model.value)
          .subscribe(data =>{
            this.alertService.alertMessage("Rescan Successfully","success","check");
          $("#rescan-part-modal").modal("hide");
    });
  }else{
    // console.log(model.value);
    // console.log("Validation Error")
  }
}


PrintElem()
{
  // const invoiceIds = ['101', '102'];

  this.toyodaOperatorService.printDocument(this.current_process._id);
    // var mywindow = window.open('', 'PRINT', 'height=20,width=20');

    // mywindow.document.write(`<html><head><title> ${document.title} </title>`);
    // mywindow.document.write(`</head><body >`);
    // mywindow.document.write(`<h1> ${document.title}</h1>`);
    // mywindow.document.write(`<img alt="dd" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACUAAAAlAQAAAADt5R2uAAAAuElEQVR4nGP4DwQ/GDDJDwKnHSoYvt/ri69g+BI9MxBIhgZdBJIxO4Ds7zdFgOIfREOBav7/Ma//wfBX4Lp1BcOP0rSMCoavB42YfzD8MZMPBarniXGvYPj9fE/QD4ZfTd+sfjB8fb7s9Q+Gj+KS3hUMv8pmtFYwfOO1FwbqNTfLBOq9wMYCdMP3T4VAN8hohP9g+H5tXfEPhi/BwgxA0yKjNIDsEGVLoBtuv18CdIOM2NMKLO4HkwDpS3ofsP5lgAAAAABJRU5ErkJggg==">`);

    // // mywindow.document.write(document.getElementById(elem).innerHTML);
    // mywindow.document.write(`</body></html>`);

    // mywindow.document.close(); // necessary for IE >= 10
    // mywindow.focus(); // necessary for IE >= 10*/

    // mywindow.print();
    // mywindow.close();

    // return true;
}

}
