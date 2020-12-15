import { Component, OnInit } from '@angular/core';

const misc: any = {
  navbar_menu_visible: 0,
  active_collapse: true,
  disabled_collapse_init: 0,
};

declare var $: any;

@Component({
  selector: 'app-apps',
  templateUrl: './apps.component.html',
  styleUrls: ['./apps.component.css']
})
export class AppsComponent implements OnInit {


  constructor() { }

  capture_url = "http://localhost:3000/capture";
  setting_url = "http://localhost:4200/config/workstation";
  report_url = "http://localhost:4200/reports/defectdetail";
  training_url = "http://localhost:4400/pages/livis/datasets";
  annotate_url = "http://localhost:4400/pages/livis/datasets";
  deploy_url = "http://localhost:4400/pages/livis/deployments";
  



  ngOnInit(): void {
    const body = document.getElementsByTagName('body')[0];
    body.classList.add('sidebar-mini');

    misc.sidebar_mini_active = true;
  }

}
