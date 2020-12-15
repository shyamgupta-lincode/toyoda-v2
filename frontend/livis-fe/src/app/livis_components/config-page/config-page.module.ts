import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../app.module';
import { NgxDaterangepickerMd } from 'ngx-daterangepicker-material';


import { ShiftComponent } from './shift/shift.component';
import {ConfigsRoutes} from './config-page-routing.module';
import { WorkstationComponent } from './workstation/workstation.component';
import { PartsComponent } from './parts/parts.component';
import {NgxMaterialTimepickerModule} from 'ngx-material-timepicker';
import { EmailComponent } from './email/email.component';
import { DragDropModule } from '@angular/cdk/drag-drop';
import { SettingsComponent } from './settings/settings.component';
import { ToyodaPartsComponent } from './toyoda-parts/toyoda-parts.component';
import { ToyodaPlanningComponent } from './toyoda-planning/toyoda-planning.component';




@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(ConfigsRoutes),
    FormsModule,
    MaterialModule,
    ReactiveFormsModule,
    NgxMaterialTimepickerModule,
    DragDropModule,
    NgxDaterangepickerMd
  ],
  declarations: [
    ShiftComponent,
    WorkstationComponent,
    PartsComponent,
    EmailComponent,
    SettingsComponent,
    ToyodaPartsComponent,
    ToyodaPlanningComponent,

    
  ]
})
export class ConfigPageModule { }
