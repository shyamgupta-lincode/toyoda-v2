import { Routes } from '@angular/router';

import { LivisLoginComponent } from './livis-login.component';
import { AdminComponent } from './admin/admin.component';

export const LivisLoginRoutes: Routes = [
    {

      path: '',
      children: [ {
        path: 'login',
        component: LivisLoginComponent
    }]
    },
    {

      path: '',
      children: [ {
        path: 'admin/login',
        component: AdminComponent
    }]
    }

];