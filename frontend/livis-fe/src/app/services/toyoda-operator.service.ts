import { Injectable } from '@angular/core';
import { Observable, from} from 'rxjs';
import { retry, catchError,map } from 'rxjs/operators';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import {livisConfig} from "../../config/constants";
import {HerrorService} from "./herror.service"
const environment =  "development";
import {Router} from '@angular/router';

const environmentConfig = livisConfig[environment];
const baseUrl = environmentConfig.BASE_URL;
const httpOptions = {};

@Injectable({
  providedIn: 'root'
})
export class ToyodaOperatorService {
  isPrinting = false;
  constructor(private http: HttpClient,private hErrorService: HerrorService,
    private router: Router) { }

  startProcess(start_info): Observable<any> {
    return this.http.post<{}>(baseUrl+'toyoda/start_process/',start_info,{})
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  endProcess(end_info): Observable<any> {
    return this.http.post<{}>(baseUrl+'toyoda/end_process/',end_info,{})
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  updateInspectionQc(inspection_info)
  {
    return this.http.post<{}>(baseUrl+'toyoda/update_manual_qc/',inspection_info,{})
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  ); 
  }

  getRunningProcess(workstation_id): Observable<any> {
    return this.http.get<{}>(baseUrl+'toyoda/get_running_process/'+workstation_id,{})
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  rescanProcess(rescan_onfo)
  {
    return this.http.post<{}>(baseUrl+'toyoda/update_manual_qc/',rescan_onfo,{})
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );  
  }

  getMetrix(inception_id): Observable<any> {
    return this.http.get<{}>(baseUrl+'reports/get_metrics/'+inception_id,{})
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  }

  getDefectList(inception_id): Observable<any> {
    return this.http.get<{}>(baseUrl+'reports/get_defect_list/'+inception_id,{})
    .pipe(map(data => {
      return data;
    }),catchError(this.hErrorService.handleError.bind(this))
    );
  }

  getCameraFeed(workstation_id): Observable<any> {
    return this.http.get<{}>(baseUrl+'toyoda/getCameraFeeds/'+workstation_id,{})
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  getProcessSummary(process_id): Observable<any> {
    return this.http.get<{}>(baseUrl+'reports/getSummary/'+process_id,{})
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  modifyPlannedProduction(product_info): Observable<any> {
    return this.http.post<{}>(baseUrl+'toyoda/plan_production_counter_modify/',product_info,{})
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

 
  printDocument(process_id) {
    this.isPrinting = true;
    this.router.navigate(['/operator/print'],{ queryParams: { process_id: process_id } });
     
  }

  onDataReady() {
    setTimeout(() => {
      window.print();
      this.isPrinting = false;
      this.router.navigate(['operator']);
    });
  }

  getQrCode()
  {
    return this.http.get<{}>(baseUrl+'toyoda/generate_QRcode/',{})
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }
  
}
