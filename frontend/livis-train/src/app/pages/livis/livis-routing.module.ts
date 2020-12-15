import { NotFoundComponent } from './../miscellaneous/not-found/not-found.component';
import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { LivisComponent } from './livis.component';
import { DatasetsComponent } from './datasets/datasets.component';
import { DeploymentsComponent } from './deployments/deployments.component';
import { WorkstationsComponent } from './workstations/workstations.component';
import { TrainingComponent } from './training/training.component';


const routes: Routes = [{
  path: '',
  component: LivisComponent,
  children: [
    {
      path: 'datasets',
      component: DatasetsComponent,
    },
    {
      path: 'deployments',
      component: DeploymentsComponent,
    },
    {
      path: 'workstations',
      component: WorkstationsComponent,
    },
    {
      path: 'training',
      component: TrainingComponent,
    },
    {
      path: '',
      redirectTo: 'datasets',
      pathMatch: 'full',
    },
    {
      path: '**',
      component: NotFoundComponent,
    },
  ],
}, {
  path: '**',
  redirectTo: 'datasets',
}];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule],
})
export class LivisRoutingModule {
}
