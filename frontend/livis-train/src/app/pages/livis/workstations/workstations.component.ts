import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';

import { NbDialogService } from '@nebular/theme';

import { LivisService } from '../livis.service';
import { DialogWorkstationCreateComponent } from './dialog-workstation-create/dialog-workstation-create.component';
import { DialogWorkstationViewComponent } from './dialog-workstation-view/dialog-workstation-view.component';
import { Workstation } from '../livis';

@Component({
  selector: 'ngx-deployments-page',
  templateUrl: 'workstations.component.html',
  styleUrls: ['workstations.component.scss'],
})
export class WorkstationsComponent implements OnInit {
  @ViewChild('input', { static: true }) input: ElementRef;

  workstations: Workstation[] = null;
  isInputShown: boolean = false;
  search_text: string = '';
  copy = (obj) => Object.assign({}, obj);

  showInput() {
    this.isInputShown = true;
    this.input.nativeElement.focus();
  }

  hideInput() {
    this.isInputShown = false;
  }

  constructor(private livisService: LivisService, private dialogService: NbDialogService) {}

  ngOnInit() {
    this.fetchWorkstations();
  }

  fetchWorkstations() {
    this.livisService.get_workstations().subscribe((data) => (this.workstations = data));
  }


  viewWorkstation(workstation) {
    this.dialogService.open(DialogWorkstationViewComponent,
      {context: {workstation: workstation}, closeOnBackdropClick: false, closeOnEsc: false})
      .onClose.subscribe(ws => {
        if (
          ws.workstation_name && ws.camera_config && ws.camera_config.cameras && ws.camera_config.cameras.length > 0) {
          ws && this.livisService.update_workstation(ws).subscribe(data => {
            const idx = this.workstations.findIndex(c => c._id === data._id);
            this.workstations[idx] = data;
          });
        }
      });
  }

  createWorkstation() {
    this.dialogService.open(DialogWorkstationCreateComponent, {closeOnBackdropClick: false, closeOnEsc: false})
      .onClose.subscribe(workstation => {
        if (
          workstation.workstation_name &&
          workstation.camera_config &&
          workstation.camera_config.cameras &&
          workstation.camera_config.cameras.length > 0
        ) {
          workstation &&
            this.livisService
              .create_workstation(workstation)
              .subscribe((ws) => this.workstations.push(ws));
        }
      });
  }
}
