import { Component } from '@angular/core';
// import {StorageService} from '../../helpers/storage.service'

@Component({
    selector: 'app-footer-cmp',
    templateUrl: 'footer.component.html'
})

export class FooterComponent {
    test: Date = new Date();
    user_deatail = localStorage.getItem('user');
}
