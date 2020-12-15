import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';

import { NbDialogService } from '@nebular/theme';

import { LivisService } from './../livis.service';
import { DialogDeploymentViewComponent } from './dialog-depolyment-view/dialog-deployment-view.component';

@Component({
  selector: 'ngx-deployments-page',
  templateUrl: 'deployments.component.html',
  styleUrls: ['deployments.component.scss'],
})
export class DeploymentsComponent implements OnInit {
  @ViewChild('input', { static: true }) input: ElementRef;

  deployments: any = null;
  isInputShown: boolean = false;
  search_text: string = '';

  constructor(private livisService: LivisService, private dialogService: NbDialogService) {}

  showInput() {
    this.isInputShown = true;
    this.input.nativeElement.focus();
  }

  hideInput() {
    this.isInputShown = false;
  }

  ngOnInit() {
    this.fetchDeployments();
  }

  fetchDeployments() {
    this.livisService.get_deployments().subscribe((data) => (this.deployments = data));
  }

  viewDeployment(deployment) {
    this.dialogService.open(DialogDeploymentViewComponent, {context: {deployment: deployment}})
      .onClose.subscribe(_ => {
        return 0;
      });
  }
}
