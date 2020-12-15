import { Component, ViewChild, OnInit } from '@angular/core';
import { NbDialogRef } from '@nebular/theme';
import { NgForm } from '@angular/forms';


@Component({
  selector: 'ngx-dialog-deployment-view',
  templateUrl: 'dialog-workstation-create.component.html',
  styleUrls: ['dialog-workstation-create.component.scss'],
})
export class DialogWorkstationCreateComponent implements OnInit {

  workstation_name: string;
  cameras: any[] = [];
  camera_name: string;
  camera_id: string;

  objectKeys = (item) => item ? Object.keys(item) : [];

  @ViewChild('cameraForm') cameraForm: NgForm;

  constructor(protected ref: NbDialogRef<DialogWorkstationCreateComponent>) {}

  ngOnInit() {}

  create() {
    const workstation = {
      workstation_name: this.workstation_name,
      camera_config: {
        cameras: this.cameras,
      },
    };
    this.ref.close(workstation);
  }

  addCamera() {
    this.cameras.push({
      camera_name: this.camera_name,
      camera_id: this.camera_id,
    });
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
}
