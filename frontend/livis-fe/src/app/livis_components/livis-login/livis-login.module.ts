import { NgModule } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MdModule } from '../../md/md.module';
import { MaterialModule } from '../../app.module';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { LivisLoginComponent } from './livis-login.component';
import { LivisLoginRoutes } from './livis-login.routing';
import { AdminComponent } from './admin/admin.component';

@NgModule({
    imports: [
        CommonModule,
        RouterModule.forChild(LivisLoginRoutes),
        MdModule,
        MaterialModule,
        FormsModule,
        ReactiveFormsModule,
    ],
    declarations: [LivisLoginComponent, AdminComponent]
})

export class LivisLoginModule {}