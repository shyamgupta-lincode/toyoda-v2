import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { NbDialogService } from '@nebular/theme';
import { LivisService } from './../livis.service';
import { NbToastrService } from '@nebular/theme';
import { DialogTrainingViewComponent } from './dialog-training-view/dialog-training-view.component';

@Component({
  selector: 'ngx-training',
  templateUrl: './training.component.html',
  styleUrls: ['./training.component.scss']
})
export class TrainingComponent implements OnInit {
  @ViewChild('input', { static: true }) input: ElementRef;
  deployments: any = null;
  isInputShown: boolean = false;
  search_text: string = '';
  constructor(private livisService:LivisService,private dialogService: NbDialogService) { }

 
  ngOnInit() {
    this.fetchDeployments();
  }

  fetchDeployments() {
    this.livisService.get_trainings().subscribe((data) => {
      console.log(data);
      this.deployments = data.running_experiments
    });
  }

  showInput() {
    this.isInputShown = true;
    this.input.nativeElement.focus();
  }

  hideInput() {
    this.isInputShown = false;
  }
  
  viewDeployment(deployment)
  {
    this.dialogService.open(DialogTrainingViewComponent, {context: {deployment: deployment}})
      .onClose.subscribe(_ => {
        return 0;
      });
  }

}
