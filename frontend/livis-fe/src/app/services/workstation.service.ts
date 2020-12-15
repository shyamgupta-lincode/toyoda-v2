import { Injectable } from '@angular/core';
import { Observable, from} from 'rxjs';
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
export class WorkstationService {

  constructor(private http: HttpClient,private hErrorService: HerrorService) { }

  getWorkStations(): Observable<any> {
    return this.http.get<{}>(baseUrl+'workstations/get_workstations/',{})
    .pipe(map(data => {
      console.log(data);
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  //add workstation

  addWorkStation(workstation_info): Observable<any> {
    return this.http.post<any>(baseUrl+'workstations/add_workstation/', JSON.stringify(workstation_info), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  getWorkStation(id): Observable<any> {
    return this.http.get<{}>(baseUrl+'workstations/workstation/'+id,{})
    .pipe(map(data => {
      console.log(data);
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  }

  updateWorkStation(workstation_info): Observable<any> {
    return this.http.patch<any>(baseUrl+'workstations/update_workstation/', JSON.stringify(workstation_info), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  deleteWorkStation(workstation_id): Observable<any> {
    return this.http.delete<any>(baseUrl+'workstations/delete_workstation/'+workstation_id, httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }



}
