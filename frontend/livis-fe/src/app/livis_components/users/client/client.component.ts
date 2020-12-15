import { Component, OnInit, ViewChild,ViewEncapsulation } from '@angular/core';
import { MatSort} from '@angular/material/sort';
import {MatPaginator} from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';
import swal from 'sweetalert2';
import {FormBuilder, FormGroup, Validators } from '@angular/forms';
import {ToyodaPartService} from "../../../services/toyoda-part.service";
import {AlertService} from '../../../services/alert.service';
import { StorageService } from '../../../helpers/storage.service';

declare const $: any;

@Component({
  selector: 'app-client',
  templateUrl: './client.component.html',
  styleUrls: ['./client.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class ClientComponent implements OnInit {
  availables:any;
  features:any;
  defects:any;
  clientForm: FormGroup;
  clientFormEdit: FormGroup;
  dataLength:number;
  isSubmitted = false;
  isSubmitedEdit = false;
  displayedColumns = ['sl', 'client_name','client_license_key','client_role','assigned_to', 'client_address','operation'];
  dataSource:any;
  user_info:any;

  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort, {}) sort: MatSort;
  

  constructor(private _fb: FormBuilder,private toyodaPartService:ToyodaPartService,
    private alertService:AlertService,
    private storageService:StorageService) 
  { }

  ngAfterViewInit() {
  }
  ngOnInit(): void {
    this.user_info = this.storageService.getUserDetails();
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
    // this.toyodaPartService.getParts()
    //   .subscribe(data =>{
      var data = [{
       "_id":"sdds",
        "client_name": "toyoda",
        "client_license_key": 4,
        "client_role": "client",
        "assigned_to": "d4f13a0b-eb09-4822-a6d7-52d556444a48",
        "client_address": "BTM banglore"
      }];

        this.dataSource = new MatTableDataSource(data);
        this.dataSource.data = data;
        this.dataLength = data.length;

        this.dataSource.paginator = this.paginator;
        this.dataSource.sort = this.sort;
      // });
    
  }
  loadAddForm()
  {
    this.clientForm = this._fb.group({
      client_name: ['', [Validators.required, ]],
      client_license_key: ['', [Validators.required, ]],
      client_role: ['client', [Validators.required]],
      assigned_to: [this.user_info.user_id, [Validators.required]],
      client_address:['', ],
     
    });
  }
  

  loadEditForm()
  {
    this.clientFormEdit = this._fb.group({
      client_name: ['', [Validators.required, ]],
      _id: ['', [Validators.required, ]],
      client_license_key: ['', [Validators.required, ]],
      client_address:['', ],
    });
  }

  filterParts(value: string):void{
    this.dataSource.filter = value.trim().toLowerCase();
  }

  addClients()
  {
    $("#add-client-modal").modal("show");
  }

  addNewClient(model)
  {
    this.isSubmitted = true;
    console.log(model.value);
    if(!this.clientForm.invalid){
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

  editClient(id)
  {
    // this.toyodaPartService.getPart(id)
    //   .subscribe(data =>{
      var data:any = {
        "_id":"sdds",
         "client_name": "toyoda",
         "client_license_key": 4,
         "client_role": "client",
         "assigned_to": "d4f13a0b-eb09-4822-a6d7-52d556444a48",
         "client_address": "BTM banglore"
       };

        this.clientFormEdit.patchValue({
          _id: data._id,
          client_name:data.client_name,
          client_license_key: data.client_license_key,
          client_address: data.client_address,
        });
        $("#edit-client-modal").modal("show");
      
    // });
    
  }

  updateClientInfo(model)
  {
    // console.log(model.value);
    this.isSubmitedEdit = true;
    if(!this.clientFormEdit.invalid){
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
