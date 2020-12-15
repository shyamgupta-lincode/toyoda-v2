import { Injectable } from '@angular/core';
import {throwError } from 'rxjs';
import {AlertService} from "../services/alert.service";

@Injectable({
  providedIn: 'root'
})
export class HerrorService {
  hErrorService:any;
  constructor(private alertNotification:AlertService)
   {

    }

  handleError(error) {

    let errorMessage = '';
    let errorStatus:any = '';
 
    if (error.error instanceof ErrorEvent) {
 
      // client-side error

 
      errorMessage = `Error: ${error.error.message}`;
      errorStatus = ''
 
    } else {
 
      // server-side error
      
      errorMessage = error.error;
      errorStatus = error.status;

 
    }
    console.log(typeof errorStatus);
    // console.log(this);
    // console.log(error);
    // window.alert(errorMessage);
    // this.alertNotification.error("dd");
    // localStorage.setItem('user', "{token:123367}");
    if(errorStatus === 400)
    {
      this.hErrorService.alertNotification.alertMessage('Bad Request','danger','error')
    }else if(errorStatus === 401)
    {
      this.hErrorService.alertNotification.alertMessage('Authentication Failed','danger','error')
    }else{
      this.hErrorService.alertNotification.alertMessage('Unknown Error','danger','error')
    }
    // if(errorMessage){
    //   this.hErrorService.alertNotification.alertMessage(errorMessage,'danger','error')
    // }else{
    //   this.hErrorService.alertNotification.alertMessage("Unknown Error",'danger','error')
    // }
 
    return throwError(errorMessage);
 
  }
}
