import { Injectable } from '@angular/core';
import { Observable, from} from 'rxjs';
import { retry, catchError,map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {livisConfig} from "../../config/constants";
import {HerrorService} from "./herror.service"
const environment =  "development";
const environmentConfig = livisConfig[environment];
const baseUrl = environmentConfig.BASE_URL;
const wbaseUrl = environmentConfig.W_BASE_URL;

const httpOptions = {};


@Injectable({
  providedIn: 'root'
})
export class OperatorService {

  constructor(private http: HttpClient,private hErrorService: HerrorService) { }

  getModelInfo(model_info): Observable<any> {
    return this.http.post<any>(baseUrl+'get_modelInfo/', JSON.stringify(model_info), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  createProcess(process_info): Observable<any> {
    return this.http.post<any>(baseUrl+'sendCreateProcess/', JSON.stringify(process_info), httpOptions)
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  
  }

  endProcess(end_process_info): Observable<any> {
    return this.http.post<any>(baseUrl+'endProcess/', JSON.stringify(end_process_info), httpOptions)
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  
  }

  checkProcess(workstation_id): Observable<any> {
    return this.http.get<{}>(baseUrl+'checkProcess/'+workstation_id,{})
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  }
  previousProcess(workstation_id): Observable<any> {
    return this.http.get<{}>(baseUrl+'get_previous_process/'+workstation_id,{})
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  }

  getMetrix(inception_id): Observable<any> {
    return this.http.get<{}>(baseUrl+'cataler/'+inception_id+'/get_metrics/',{})
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  }

  getDefectList(inception_id): Observable<any> {
    return this.http.get<{}>(baseUrl+'cataler/'+inception_id+'/get_defect_list/',{})
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  }

  updateOcr(ocr_info): Observable<any> {
    return this.http.post<any>(baseUrl+'update_inspection_result/', JSON.stringify(ocr_info), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  getProcessSummary(process_id): Observable<any> {
    return this.http.get<{}>(baseUrl+'getSummary/'+process_id,{})
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  }

  getcameraFeed(workstation_id): Observable<any> {
    return this.http.get<{}>(baseUrl+'getCameraFeeds/'+workstation_id,{})
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  }

 

}
