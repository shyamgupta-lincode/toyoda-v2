import { Routes } from '@angular/router';

import { ClientComponent } from './client/client.component';



export const UsersRoutingModule: Routes = [
    {
      path: '',
      children: [ {
        path: 'clients',
        component: ClientComponent
    }]}, 
  
  
    // {
    // path: '',
    // children: [ {
    //   path: 'grid',
    //   component: GridSystemComponent
    // }]
    // }
];
