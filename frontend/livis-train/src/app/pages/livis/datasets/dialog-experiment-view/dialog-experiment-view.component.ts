import { Component, Input, OnInit } from '@angular/core';
import { NbDialogRef, NbDialogService } from '@nebular/theme';

import { LivisService } from '../../livis.service';
import { Workstation } from '../../livis';
import { WorkstationChooseComponent } from './workstation-choose/workstation-choose.component';
import { NbToastrService } from '@nebular/theme';

@Component({
  selector: 'ngx-dialog-experiment-prompt',
  templateUrl: 'dialog-experiment-view.component.html',
  styleUrls: ['dialog-experiment-view.component.scss'],
  providers: [LivisService],
})
export class DialogExperimentViewComponent implements OnInit {

  @Input() dataset: any;
  @Input() exp: any;

  objectKeys = (item) => item ? Object.keys(item) : [];
  deployRequested: boolean = false;
  deployed: boolean = false;
  workstations: Workstation[] = [];
  depolyed_on: Workstation[] = [];

  constructor(
    protected ref: NbDialogRef<DialogExperimentViewComponent>,
    private livisService: LivisService,
    private dialogService: NbDialogService,
    private toastrService: NbToastrService
  ) {}

  ngOnInit() {
    this.deployed = !!(this.exp && this.exp.deployed);
    this.livisService.get_workstations().subscribe(w => this.workstations = w);
    if (this.deployed && this.exp.deployed_on_workstations && this.exp.deployed_on_workstations.length > 0) {
      this.exp.deployed_on_workstations.forEach(ws_id => {
        this.livisService.get_workstation(ws_id).subscribe(w => this.depolyed_on.push(w));
      });
    }
  }

  getLabelwiseReport() {
    console.log(this.exp);
    const train_status = this.exp.train_status;
    const labelwise = train_status && train_status.report && train_status.report || {};
    return Object.keys(labelwise).map(key => [key, labelwise[key]]);
  }

  getConfusionMatrix() {
    // console.log(this.exp);
    const train_status = this.exp.train_status;
    return train_status && train_status.confusion_matrix || [];
  }

  getOverallSupport() {
    const train_status = this.exp.train_status;
    const overall = train_status && train_status.report && train_status.report.overall || {};
    return overall.support;
  }

  getBgColor(item) {
    const support = this.getOverallSupport();
    const opacity = parseFloat(item) / support;
    return `rgba(255, 255, 255, ${1 - opacity})`;
  }

  deploy() {
    this.dialogService.open(WorkstationChooseComponent,
      {context: {workstations: this.workstations}, closeOnBackdropClick: false, closeOnEsc: false})
      .onClose.subscribe(selected_workstations => {
        if (selected_workstations.length < 1) {
          return;
        }
        this.deployRequested = true;
        this.deployed = true;
        this.livisService
          .deploy_experiment(this.dataset._id, this.exp._id, selected_workstations)
          .subscribe((_) => {
            this.toastrService.success('Deploy Successfully')
            this.ref.close(1)
          });
      });
  }

  cancel() {
    this.ref.close();
  }

  submit() {
    this.ref.close();
  }
}
