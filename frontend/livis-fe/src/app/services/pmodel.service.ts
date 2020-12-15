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
export class PmodelService {


  constructor(private http: HttpClient,private hErrorService: HerrorService) { }

  getModels(): Observable<any> {
    return this.http.get<{}>(baseUrl+'get_parts/',httpOptions)
    .pipe(map(data => {
      // console.log(data);
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  getModel(id): Observable<any> {
    return this.http.get<{}>(baseUrl+'part/'+id,{})
    .pipe(map(data => {
      // console.log(data);
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  //add workstation

  addModel(model_info): Observable<any> {
    return this.http.post<any>(baseUrl+'add_part/', JSON.stringify(model_info), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  updateModel(model_info): Observable<any> {
    return this.http.post<any>(baseUrl+'update_part/', JSON.stringify(model_info), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  deleteModel(model_info): Observable<any> {
    return this.http.post<any>(baseUrl+'delete_part/', JSON.stringify(model_info), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  

}


