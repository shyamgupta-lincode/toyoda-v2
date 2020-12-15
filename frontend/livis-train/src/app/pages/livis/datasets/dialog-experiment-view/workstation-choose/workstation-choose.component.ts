import { Component, Input } from '@angular/core';
import { NbDialogRef } from '@nebular/theme';

@Component({
  selector: 'ngx-dialog-experiment-prompt',
  templateUrl: 'workstation-choose.component.html',
  styleUrls: ['workstation-choose.component.scss'],
})
export class WorkstationChooseComponent {

  @Input() workstations: any;

  selected_workstations: any;

  constructor(protected ref: NbDialogRef<WorkstationChooseComponent>) {}

  cancel() {
    this.ref.close();
  }

  submit() {
    const sw = this.selected_workstations.map(ws => ws._id);
    this.ref.close(sw);
  }
}
