import { Component, OnInit, ElementRef, OnDestroy } from '@angular/core';
import { FormGroup, FormControl,FormBuilder,Validators } from '@angular/forms';
import { AuthenticationService } from '../../../services/authentication.service';
import {Router} from '@angular/router'
import {AlertService} from '../../../services/alert.service'
import { from } from 'rxjs';




declare var $: any;

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent implements OnInit {
  loginForm;
  isSubmitted = false;
  

  test: Date = new Date();
  private toggleButton: any;
  private sidebarVisible: boolean;
  private nativeElement: Node;

  constructor(private element: ElementRef,
    private authenticationService: AuthenticationService,
    private formBuilder: FormBuilder,
    private router:Router,
    private alertService:AlertService) {
      this.nativeElement = element.nativeElement;
      this.sidebarVisible = false;
      if(localStorage.getItem('user'))
      {
        
        let user_info = JSON.parse(localStorage.getItem('user'));
        // console.log(user_info['role_name']);
        
        if(user_info['role_name'] == 'sys admin')
        {
          this.router.navigate(['livis/apps']);
        }
        
      }
      
      // this.loginForm = formBuilder.group({
      //   email: ['',Validators.required],
      //   password: ['',Validators.required],
      //   workstation_name:['',Validators.required],
      // });
  }


  

  selectTheme = 'primary';

  workstations:{};
  getWorkStations(): void {
  this.authenticationService.getWorkStations()
    .subscribe(workstations => this.workstations = workstations);
    // this.workstations = this.loginService.getWorkStations();
  }

  // 
  // cities = [
  //   {value: '1', viewValue: 'Workstatation1'},
  //   {value: '1', viewValue: 'Workstatation2'},
  //   {value: '1', viewValue: 'Workstatation3'},

    
  // ];

  ngOnInit() {
    
    var navbar : HTMLElement = this.element.nativeElement;
    this.toggleButton = navbar.getElementsByClassName('navbar-toggle')[0];
    const body = document.getElementsByTagName('body')[0];
    body.classList.add('login-page');
    body.classList.add('off-canvas-sidebar');
    const card = document.getElementsByClassName('card')[0];
    setTimeout(function() {
        // after 1000 ms we add the class animated to the login/register card
        card.classList.remove('card-hidden');
    }, 700);
    this.getWorkStations();
    this.loginForm = this.formBuilder.group({
      email: ['', [Validators.required]],
      password: ['', Validators.required],
      // workstation_name:['',Validators.required],
   });
  }

  sidebarToggle() {
    var toggleButton = this.toggleButton;
    var body = document.getElementsByTagName('body')[0];
    var sidebar = document.getElementsByClassName('navbar-collapse')[0];
    if (this.sidebarVisible == false) {
        setTimeout(function() {
            toggleButton.classList.add('toggled');
        }, 500);
        body.classList.add('nav-open');
        this.sidebarVisible = true;
    } else {
        this.toggleButton.classList.remove('toggled');
        this.sidebarVisible = false;
        body.classList.remove('nav-open');
    }
  }
  ngOnDestroy(){
    const body = document.getElementsByTagName('body')[0];
    body.classList.remove('login-page');
    body.classList.remove('off-canvas-sidebar');
  }

  // validateAllFormFields(formGroup: FormGroup) {
  //   Object.keys(formGroup.controls).forEach(field => {
  //     const control = formGroup.get(field);
  //     if (control instanceof FormControl) {
  //       control.markAsTouched({ onlySelf: true });
  //     } else if (control instanceof FormGroup) {
  //       this.validateAllFormFields(control);
  //     }
  //   });
  // }

  get formControls() { 
    return this.loginForm.controls; 
  }

  loginUser(event) {

    // console.log(this.loginForm.value);
    
    this.isSubmitted = true;
    if(this.loginForm.invalid){
      return;
    }
    this.authenticationService.adminLogin(this.loginForm.get('email').value,this.loginForm.get('password').value)
        .subscribe(data =>{
          // console.log(data,data['role_name'])
          // localStorage.setItem('user', JSON.stringify(data));
          if(data['role_name'] == "sys admin"){
            this.alertService.alertMessage("Login Successfully","success","check");
            this.router.navigate(['livis/apps'])
          }else{
            this.alertService.alertMessage("Failed!!!",'danger','error');
          }
          
          // console.log(data)
        });
   
    // console.log(this.loginForm.value);
    // this.router.navigateByUrl('/admin');
    // event.preventDefault();
    // console.log(this.loginForm.get('email').value);
    // console.log(event);
    // return false;
    // if (this.loginForm.valid) {
    //   console.log(this.loginForm.value);
    // } else {
    //   console.log(this.loginForm.value);
    //   this.validateAllFormFields(this.loginForm);
    // }
  
  }
  


}
