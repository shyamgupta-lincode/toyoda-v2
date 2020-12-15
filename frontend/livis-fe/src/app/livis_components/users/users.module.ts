import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MaterialModule } from '../../app.module';
import { NgxDaterangepickerMd } from 'ngx-daterangepicker-material';

import { UsersRoutingModule } from './users-routing.module';
import { ClientComponent } from './client/client.component';


@NgModule({
  imports: [
    CommonModule,
    RouterModule.forChild(UsersRoutingModule),
    FormsModule,
    MaterialModule,
    ReactiveFormsModule,
    NgxDaterangepickerMd
  ],
  declarations: [
    ClientComponent,
    
    
  ]
})

export class UsersModule { }
