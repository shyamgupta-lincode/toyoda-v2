import { Routes } from '@angular/router';

import { ShiftComponent } from './shift/shift.component';
import { WorkstationComponent } from './workstation/workstation.component';
import {PartsComponent} from "./parts/parts.component";
import {EmailComponent} from "./email/email.component";
import {SettingsComponent} from "./settings/settings.component";
import { ToyodaPartsComponent } from './toyoda-parts/toyoda-parts.component';
import { ToyodaPlanningComponent } from './toyoda-planning/toyoda-planning.component';



export const ConfigsRoutes: Routes = [
    {
      path: '',
      children: [ {
        path: 'shift',
        component: ShiftComponent
    }]}, 
    {
      path: '',
      children: [ {
        path: 'workstation',
        component: WorkstationComponent
    }]}, 
    {
      path: '',
      children: [ {
        path: 'part',
        component: ToyodaPartsComponent
    }]}, 
    {
      path: '',
      children: [ {
        path: 'email',
        component: EmailComponent
    }]}, 
    {
      path: '',
      children: [ {
        path: 'settings',
        component: SettingsComponent
    }]}, 
    {
      path: '',
      children: [ {
        path: 'planning',
        component: ToyodaPlanningComponent
    }]}, 
    // {
    // path: '',
    // children: [ {
    //   path: 'grid',
    //   component: GridSystemComponent
    // }]
    // }
];
