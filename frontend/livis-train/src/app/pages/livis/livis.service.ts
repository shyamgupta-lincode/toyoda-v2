import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {
  Dataset,
  UploadResponse,
  DatasetPayload,
  DatasetResponse,
  ExperimentPayload,
  Workstation,
  WorkstationPayload,
} from './livis';

@Injectable()
export class LivisService {

  baseApiURL = 'http://164.52.194.78:2323/livis/v1/';

  constructor(private http: HttpClient) {}

  load_datasets(): Observable<Dataset[]> {
    return this.http.get<Dataset[]>(this.baseApiURL + 'parts/get_all_parts/');
  }

  upload_file(file: File): Observable<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<UploadResponse>(this.baseApiURL + 'upload/', formData);
  }

  create_dataset(payload: DatasetPayload): Observable<DatasetResponse> {
    return this.http
      .post<DatasetResponse>(this.baseApiURL + 'parts/add_part/', payload);
  }

  create_experiment(payload: any, obj_id: string): Observable<Dataset> {
    // payload.part_id = payload.u
    return this.http.post<Dataset>(this.baseApiURL + 'training/create_experiment/', payload);
  }

  deploy_experiment(dataset_id: string, experiment_id: string, workstation_ids: string[]): Observable<any> {
    return this.http.post<any>(
      this.baseApiURL + 'training/deploy_experiment/', {part_id:dataset_id,experiment_id:experiment_id, workstation_ids:workstation_ids});
  }

  get_deployments(): Observable<any> {
    return this.http.get<any>(this.baseApiURL + 'training/get_deployment_list/');
  }

  get_trainings(): Observable<any> {
    return this.http.get<any>(this.baseApiURL + 'training/get_all_running_experiments/');
  }

  get_workstations(): Observable<Workstation[]> {
    return this.http.get<Workstation[]>(this.baseApiURL + 'workstations/get_workstations/');
  }

  get_workstation(ws_id): Observable<Workstation> {
    return this.http.get<Workstation>(this.baseApiURL + 'v1/workstation/' + ws_id + '/');
  }

  create_workstation(payload: WorkstationPayload): Observable<Workstation> {
    return this.http.post<any>(this.baseApiURL + 'add_workstation/', payload);
  }

  update_workstation(payload: any): Observable<any> {
    return this.http.post<any>(this.baseApiURL + 'update_workstation/', payload);
  }
}
