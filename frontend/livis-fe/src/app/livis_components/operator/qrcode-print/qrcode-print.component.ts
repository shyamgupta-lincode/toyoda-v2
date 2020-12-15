import { Component, OnInit,ViewEncapsulation } from '@angular/core';
import {ToyodaOperatorService} from '../../../services/toyoda-operator.service';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-qrcode-print',
  templateUrl: './qrcode-print.component.html',
  styleUrls: ['./qrcode-print.component.css'],
  encapsulation: ViewEncapsulation.None
})
export class QrcodePrintComponent implements OnInit {


  invoiceIds: string[];
  invoiceDetails: Promise<any>[];
  image_src:any = "";
  process_id:any = "";

  constructor(private route: ActivatedRoute,
              private toyodaOperatorService: ToyodaOperatorService) {
    // this.invoiceIds = ['100','111'];
  }

  ngOnInit() {
    this.route.queryParams
      .filter(params => params.process_id)
      .subscribe(params => {
        console.log(params); // { order: "popular" }
        // this.process_id = params.process_id;
        this.toyodaOperatorService.getDefectList(params.process_id).subscribe(data =>{
          // console.log(data);
          //  Promise.all(this.image_src = data.qr_string)
          //   .then(() => this.toyodaOperatorService.onDataReady());
          this.image_src = data.qr_string;
          this.toyodaOperatorService.onDataReady();
        });
        // console.log(this.order); // popular
      }
    );

    // this.invoiceDetails = this.invoiceIds
    //   .map(id => this.getInvoiceDetails(id));
    // Promise.all(this.invoiceDetails)
    //   .then(() => this.toyodaOperatorService.onDataReady());
  }

  getInvoiceDetails(invoiceId) {
    const amount = Math.floor((Math.random() * 100));
    return new Promise(resolve =>
      setTimeout(() => resolve({amount}), 1000)
    );
  }

}
