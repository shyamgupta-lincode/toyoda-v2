import { Component, Input, OnInit } from '@angular/core';
import { NbDialogRef } from '@nebular/theme';

import { LivisService } from '../../livis.service';

@Component({
  selector: 'ngx-dialog-deployment-view',
  templateUrl: 'dialog-deployment-view.component.html',
  styleUrls: ['dialog-deployment-view.component.scss'],
  providers: [LivisService],
})
export class DialogDeploymentViewComponent implements OnInit {

  @Input() deployment: any;

  objectKeys = (item) => item ? Object.keys(item) : [];

  constructor(protected ref: NbDialogRef<DialogDeploymentViewComponent>) {}

  ngOnInit() {}

  deploy() {
  }

  cancel() {
    this.ref.close();
  }

  submit() {
    this.ref.close();
  }
}
