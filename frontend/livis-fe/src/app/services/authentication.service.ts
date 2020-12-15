import { Injectable } from '@angular/core';
import { Observable, from,} from 'rxjs';
import { retry, catchError,map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {livisConfig} from "../../config/constants";
import {HerrorService} from "./herror.service"
const environment =  "development";
const environmentConfig = livisConfig[environment];
const baseUrl = environmentConfig.BASE_URL;
const httpOptions = {};
@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {

  constructor( private http: HttpClient,private hErrorService: HerrorService) {

   }

  getWorkStations():Observable<{}> {

    return this.http.get<{}>(baseUrl+'workstations/get_workstations/')
    // console.log(baseUrl+'accounts/api/v1/login');
    // return of([
    //   {value: '1', viewValue: 'Workstatation1'},
    //   {value: '1', viewValue: 'Workstatation2'},
    //   {value: '1', viewValue: 'Workstatation3'},
    // ]);
  }

  userLogin(email,password,workstation_name): Observable<{}> {
    return this.http.post<{}>(baseUrl+'accounts/login/', {email:email,password:password,workstation_name:workstation_name}, httpOptions)
    .pipe(map(user_info => {
      user_info['workstation_id'] = workstation_name;
      // user_info['name'] = "Shyam";
      // user_info['role'] = "System Admin";
      // user_info['user_id'] = "5ef5005a-5473-440b-ab29-272a810da5d3";


      // window.Data1 = 
      // gwindow.$livis_user_info = 
      // store user details and jwt token in local storage to keep user logged in between page refreshes
      localStorage.setItem('user', JSON.stringify(user_info));
      // localStorage.setItem('workstation_id', workstation_name);
      return user_info;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  adminLogin(email,password): Observable<{}> {
    return this.http.post<{}>(baseUrl+'accounts/login/', {email:email,password:password,workstation_name:"dd"}, httpOptions)
    .pipe(map(user_info => {
      // user_info['workstation_id'] = workstation_name;
      // user_info['name'] = "Shyam";
      // user_info['role'] = "System Admin";
      // user_info['user_id'] = "5ef5005a-5473-440b-ab29-272a810da5d3";
      // store user details and jwt token in local storage to keep user logged in between page refreshes
      if(user_info['role_name'] == 'sys admin'){
        // alert("hi");
        localStorage.setItem('user', JSON.stringify(user_info));
      }
      // localStorage.setItem('workstation_id', workstation_name);
      return user_info;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  checkUserLogin(email,password,workstation_name): Observable<{}> {
    return this.http.post<{}>(baseUrl+'accounts/login/', {email:email,password:password,workstation_name:workstation_name}, httpOptions)
    .pipe(map(user_info => {
      return user_info;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }


logout() {
    localStorage.removeItem('user');
}

  
 
 


}
