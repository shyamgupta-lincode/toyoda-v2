import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import {
  NbAccordionModule,
  NbButtonModule,
  NbCardModule,
  NbListModule,
  NbRouteTabsetModule,
  NbStepperModule,
  NbTabsetModule,
  NbUserModule,
  NbIconModule,
  NbDialogModule,
  NbCheckboxModule,
  NbRadioModule,
  NbSelectModule,
  NbInputModule,
} from '@nebular/theme';

import { ThemeModule } from '../../@theme/theme.module';
import { LivisRoutingModule } from './livis-routing.module';
import { LivisComponent } from './livis.component';
import { DatasetsComponent } from './datasets/datasets.component';
import { DeploymentsComponent } from './deployments/deployments.component';
import { LivisService } from './livis.service';
import { FilterByPartNumberPipe } from './datasets/datasets.pipe';
import { DialogExperimentViewComponent } from './datasets/dialog-experiment-view/dialog-experiment-view.component';
import { DialogDatasetPromptComponent } from './datasets/dialog-dataset-prompt/dialog-dataset-prompt.component';
import {
  DialogExperimentPromptComponent,
} from './datasets/dialog-experiment-prompt/dialog-experiment-prompt.component';
import { DialogDeploymentViewComponent } from './deployments/dialog-depolyment-view/dialog-deployment-view.component';
import { WorkstationsComponent } from './workstations/workstations.component';
import {
  DialogWorkstationCreateComponent,
} from './workstations/dialog-workstation-create/dialog-workstation-create.component';
import {
  DialogWorkstationViewComponent,
} from './workstations/dialog-workstation-view/dialog-workstation-view.component';
import {
  WorkstationChooseComponent,
} from './datasets/dialog-experiment-view/workstation-choose/workstation-choose.component';
import { TrainingComponent } from './training/training.component';
import { DialogTrainingViewComponent } from './training/dialog-training-view/dialog-training-view.component';

@NgModule({
  imports: [
    FormsModule,
    ReactiveFormsModule,
    ThemeModule,
    NbTabsetModule,
    NbRouteTabsetModule,
    NbStepperModule,
    NbCardModule,
    NbButtonModule,
    NbListModule,
    NbAccordionModule,
    NbUserModule,
    NbIconModule,
    NbDialogModule,
    NbCheckboxModule,
    NbRadioModule,
    NbSelectModule,
    NbInputModule,
    LivisRoutingModule,
  ],
  declarations: [
    LivisComponent,
    DatasetsComponent,
    DeploymentsComponent,
    DialogDatasetPromptComponent,
    DialogExperimentPromptComponent,
    DialogExperimentViewComponent,
    DialogDeploymentViewComponent,
    WorkstationsComponent,
    DialogWorkstationViewComponent,
    DialogWorkstationCreateComponent,
    WorkstationChooseComponent,
    FilterByPartNumberPipe,
    TrainingComponent,
    DialogTrainingViewComponent,
  ],
  providers: [
    LivisService,
  ],
})
export class LivisModule { }
