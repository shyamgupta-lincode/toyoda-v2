import { Component, OnInit } from '@angular/core';
import PerfectScrollbar from 'perfect-scrollbar';
// import {StorageService} from "../helpers/storage.service";


declare const $: any;

//Metadata
export interface RouteInfo {
    path: string;
    title: string;
    type: string;
    icontype: string;
    collapse?: string;
    children?: ChildrenItems[];
}

export interface ChildrenItems {
    path: string;
    title: string;
    ab: string;
    type?: string;
}


// console.log(user_info);

//Menu Items
let dashboard_menu = null;
let config_menu = null;
let operator_menu = null;
// if(false){
// function menusetup(){    
    let user_info = JSON.parse(localStorage.getItem('user'));
    // console.log(user_info);
dashboard_menu = {
    path: '/dashboard',
    title: 'Dashboard',
    type: 'link',
    icontype: 'dashboard'
};

// }
if(user_info && user_info['role_name'] == "operator")
{
    operator_menu =  {
        path: '/operator',
        title: 'Operator',
        type: 'link',
        icontype: 'list'
    }
}
// console.log(user_info);
if(user_info && user_info['role_name'] == "sys admin")
{
    config_menu = {
        path: '/config',
        title: 'Config',
        type: 'sub',
        icontype: 'computer',
        collapse: 'config',
        children: [
            {path: 'shift', title: 'Shift Management', ab:'SM'},
            {path: 'part', title: 'Parts and Models', ab:'PM'},
            {path: 'planning', title: 'Planning', ab:'PL'},

            {path: 'workstation', title: 'Workstations', ab:'WS'},
            // {path: 'settings', title: 'Setting', ab:'ST'},
            {path: 'email', title: 'Email Setting', ab:'ES'},

           
        ]
    }; 
}
// }

// setTimeout(menusetup,2000);
export const ROUTES: RouteInfo[] = [
    // dashboard_menu,
    operator_menu,
    // {
    //     path: '/user',
    //     title: 'Users & Roles',
    //     type: 'sub',
    //     icontype: 'person',
    //     collapse: 'user',
    //     children: [
    //         {path: 'clients', title: 'Manage Clients', ab:'CL'},
    //     ]
    // },
    config_menu,

    {
        path: '/reports',
        title: 'Reports',
        type: 'sub',
        icontype: 'polls',
        collapse: 'reports',
        children: [
            {path: 'defectdetail', title: 'Defect Detail', ab:'DD'},
            // {path: 'defectTypes', title: 'Types of Defect', ab:'TOD'},
            // {path: 'productionQuality', title: 'Production Quality', ab:'PQ'},
            // {path: 'shiftSummary', title: 'Shift Summary', ab:'SS'},
           
        ]
    },
   
];
@Component({
    selector: 'app-sidebar-cmp',
    templateUrl: 'sidebar.component.html',
})

export class SidebarComponent implements OnInit {
    public menuItems: any[];
    ps: any;
    userName:any = "";
    isMobileMenu() {
        if ($(window).width() > 991) {
            return false;
        }
        return true;
    };

    ngOnInit() {
        this.menuItems = ROUTES.filter(menuItem => menuItem);
        if (window.matchMedia(`(min-width: 960px)`).matches && !this.isMac()) {
            const elemSidebar = <HTMLElement>document.querySelector('.sidebar .sidebar-wrapper');
            this.ps = new PerfectScrollbar(elemSidebar);
        }
        var user_info = JSON.parse(localStorage.getItem('user'));
        this.userName = user_info.first_name;
    }
    updatePS(): void  {
        if (window.matchMedia(`(min-width: 960px)`).matches && !this.isMac()) {
            this.ps.update();
        }
    }
    isMac(): boolean {
        let bool = false;
        if (navigator.platform.toUpperCase().indexOf('MAC') >= 0 || navigator.platform.toUpperCase().indexOf('IPAD') >= 0) {
            bool = true;
        }
        return bool;
    }
}
