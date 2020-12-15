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
export class ToyodaPlanningService {

  constructor(private http: HttpClient,private hErrorService: HerrorService) { }

  getPlannings(): Observable<any> {
    return this.http.get<{}>(baseUrl+'plan/get_plans/',{})
    .pipe(map(data => {
      // console.log(data);
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  addPlan(plan_info): Observable<any> {
    return this.http.post<{}>(baseUrl+'plan/add_plan/',plan_info,{})
    .pipe(map(data => {
      // console.log(data);
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  deletePlanning(plan_id): Observable<any> {
    return this.http.delete<{}>(baseUrl+'plan/delete_plan/'+plan_id,{})
    .pipe(map(data => {
      // console.log(data);
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  getPlanning(plan_id): Observable<any> {
    return this.http.get<{}>(baseUrl+'plan/get_plan/'+plan_id,{})
    .pipe(map(data => {
      // console.log(data);
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  updatePlan(plan_info): Observable<any> {
    return this.http.patch<{}>(baseUrl+'plan/update_plan/',plan_info,{})
    .pipe(map(data => {
      // console.log(data);
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  

}
