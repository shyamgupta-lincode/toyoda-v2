import { Routes, RouterModule } from '@angular/router';
import {OperatorPageComponent} from './operator-page/operator-page.component';
import { ToyodaOperatorComponent } from './toyoda-operator/toyoda-operator.component';
// import { QrcodePrintComponent } from './qrcode-print/qrcode-print.component';


export const OperatorRoutes: Routes = [
  {
    path: '',
    children: [ {
      path: '',
      component: ToyodaOperatorComponent
  }]},

  // {
  //   path: '',
  //   children: [ {
  //     path: 'print',
  //     component: QrcodePrintComponent
  // }]},
]
