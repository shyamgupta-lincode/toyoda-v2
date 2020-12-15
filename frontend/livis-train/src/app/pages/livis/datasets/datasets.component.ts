import { Component, OnInit, ViewChild, ElementRef } from '@angular/core';
import { NbDialogService } from '@nebular/theme';
import { DialogDatasetPromptComponent } from './dialog-dataset-prompt/dialog-dataset-prompt.component';
import { DialogExperimentPromptComponent } from './dialog-experiment-prompt/dialog-experiment-prompt.component';
import { DialogExperimentViewComponent } from './dialog-experiment-view/dialog-experiment-view.component';

import { LivisService } from '../livis.service';
import { Dataset } from '../livis';
import { NbToastrService } from '@nebular/theme';

@Component({
  selector: 'ngx-datasets',
  templateUrl: 'datasets.component.html',
  styleUrls: ['datasets.component.scss'],
})
export class DatasetsComponent implements OnInit {
  @ViewChild('input', { static: true }) input: ElementRef;

  objectKeys = Object.keys;
  search_text: string = '';
  filterargs = {part_number: this.search_text};
  datasets: Dataset[]  = [];
  isInputShown: boolean = false;

  constructor(private dialogService: NbDialogService, private livisService: LivisService,
    private toastrService: NbToastrService,) {}

  ngOnInit() {
    this.fetchDatasets();
  }

  fetchDatasets() {
    this.livisService.load_datasets().subscribe(data => this.datasets = data);
  }

  showInput() {
    this.isInputShown = true;
    this.input.nativeElement.focus();
  }

  hideInput() {
    this.isInputShown = false;
  }

  open() {
    this.dialogService.open(DialogDatasetPromptComponent, {closeOnBackdropClick: false, closeOnEsc: false})
      .onClose.subscribe(dataset => {
        dataset && this.livisService.create_dataset(dataset).subscribe(resp_data => {
          // this.datasets.push(resp_data.data);
          this.fetchDatasets();
          this.toastrService.success('Part Added Successfully');
        });
      });
  }

  addExperiment(ds) {
    this.dialogService
      .open(
        DialogExperimentPromptComponent,
        {context: {dataset: ds}, closeOnEsc: false, closeOnBackdropClick: false})
      .onClose.subscribe(experiment => {
        experiment && this.livisService.create_experiment(experiment, ds._id).subscribe(resp_data => {
          // const idx = this.datasets.findIndex(d => d._id === ds._id);
          // this.datasets[idx] = resp_data;
          this.fetchDatasets();
          this.toastrService.success('Added Successfully');
        });
      });
  }

  viewExperiment(ds, exp) {
    this.dialogService
      .open(
        DialogExperimentViewComponent,
        {context: {dataset: ds, exp: exp}, closeOnBackdropClick: false, closeOnEsc: false})
      .onClose.subscribe(res => {
        res && this.fetchDatasets()
        
      });
      
  }
  refreshPartList()
  {
    this.fetchDatasets();
  }
}
