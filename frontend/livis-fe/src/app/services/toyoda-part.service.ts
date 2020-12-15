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
export class ToyodaPartService {

  constructor(private http: HttpClient,private hErrorService: HerrorService) { }

  getParts(): Observable<any> {
    return this.http.get<{}>(baseUrl+'parts/get_all_parts/',{})
    .pipe(map(data => {
      // console.log(data);
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  getPart(id): Observable<any> {
    return this.http.get<{}>(baseUrl+'parts/part_details/'+id,{})
    .pipe(map(data => {
      // console.log(data);
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

  //add workstation

  addNewPart(model_info): Observable<any> {
    return this.http.post<any>(baseUrl+'parts/add_part/', JSON.stringify(model_info), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  updatePart(model_info): Observable<any> {
    return this.http.patch<any>(baseUrl+'parts/update_part/', JSON.stringify(model_info), httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  deletePart(part_id): Observable<any> {
    return this.http.delete<any>(baseUrl+'parts/delete_part/'+part_id, httpOptions)
    .pipe(map(data => {
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  
  }

  getPartByShortNumber(short_number): Observable<any> {
    return this.http.get<{}>(baseUrl+'parts/get_partInfo/'+short_number,{})
    .pipe(map(data => {
      // console.log(data);
      return data;
  }),catchError(this.hErrorService.handleError.bind(this))
  );
  }

}
