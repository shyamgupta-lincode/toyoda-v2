import { Component, Input, OnInit } from '@angular/core';
import { NbDialogRef } from '@nebular/theme';

import { LivisService } from '../../livis.service';

@Component({
  selector: 'ngx-dialog-training-view',
  templateUrl: './dialog-training-view.component.html',
  styleUrls: ['./dialog-training-view.component.scss']
  // providers: [LivisService],
})
export class DialogTrainingViewComponent implements OnInit {

  @Input() deployment: any;

  objectKeys = (item) => item ? Object.keys(item) : [];

  constructor(protected ref: NbDialogRef<DialogTrainingViewComponent>) {}

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
