import { Component, Input, OnInit, ViewChild } from '@angular/core';
import { NbDialogRef } from '@nebular/theme';

import { LivisService } from '../../livis.service';
import { NgForm } from '@angular/forms';

@Component({
  selector: 'ngx-dialog-deployment-view',
  templateUrl: 'dialog-workstation-view.component.html',
  styleUrls: ['dialog-workstation-view.component.scss'],
  providers: [LivisService],
})
export class DialogWorkstationViewComponent implements OnInit {

  @Input() workstation: any;
  @ViewChild('cameraForm') cameraForm: NgForm;

  objectKeys = (item) => item ? Object.keys(item) : [];
  cameras: any[] = [];
  camera_name: string;
  camera_id: string;

  constructor(protected ref: NbDialogRef<DialogWorkstationViewComponent>) {}

  ngOnInit() {
    this.cameras = this.workstation.camera_config && this.workstation.camera_config.cameras || [];
  }

  addCamera() {
    this.cameras.push({
      camera_name: this.camera_name,
      camera_id: this.camera_id,
    });
    this.workstation.camera_config.cameras = this.cameras;
    this.camera_id = '';
    this.camera_name = '';
    this.cameraForm.form.markAsPristine();
    this.cameraForm.form.markAsUntouched();
  }

  removeCamera(camera) {
    const idx = this.cameras.findIndex(c => c.camera_name === camera.camera_name);
    this.cameras.splice(idx, 1);
  }

  cancel() {
    this.ref.close();
  }

  update() {
    this.ref.close(this.workstation);
  }
}
