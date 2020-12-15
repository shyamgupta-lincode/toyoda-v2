import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../app.module';


import { OperatorPageComponent } from './operator-page/operator-page.component';
import {OperatorRoutes} from './operator-routing.module';
import { ToyodaOperatorComponent } from './toyoda-operator/toyoda-operator.component';
// import { QrcodePrintComponent } from './qrcode-print/qrcode-print.component';






@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(OperatorRoutes),
    FormsModule,
    MaterialModule,
    ReactiveFormsModule,
  ],
  declarations: [
    OperatorPageComponent,
    ToyodaOperatorComponent,
    // QrcodePrintComponent
  ]
})
export class OperatorModule { }
