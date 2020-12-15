import { Component, OnInit, ViewChild,ElementRef, OnDestroy,Input } from '@angular/core';
import { MatSort} from '@angular/material/sort';
import {MatPaginator} from '@angular/material/paginator';
import {MatTableDataSource} from '@angular/material/table';
// import '@angular/';
// import {MatDatepickerModule} from '@angular/material/datepicker';
// import {NgbDate, NgbCalendar,NgbInputDatepicker,NgbDateParserFormatter} from '@ng-bootstrap/ng-bootstrap';
declare const $: any;

@Component({
  selector: 'app-defect-types',
  templateUrl: './defect-types.component.html',
  styleUrls: ['./defect-types.component.css']
})

export class DefectTypesComponent implements OnInit {

// @ViewChild('datePicker') datePicker: NgbInputDatepicker;
// fromDate: NgbDate;
// toDate: NgbDate;
// onFirstSelection = true;


  // fromDate: NgbDate;
  // toDate: NgbDate;
  // hoveredDate: NgbDate;

  constructor() {
    // this.fromDate = calendar.getToday();
    // this.toDate = calendar.getNext(calendar.getToday(), 'd', 10);
  }
  displayedColumns;
  dataSource: MatTableDataSource<any>;
  dataLength: number;
  @ViewChild(MatPaginator) paginator: MatPaginator;
  @ViewChild(MatSort, {}) sort: MatSort;
  selectedRowIndex: number = -1;
  ngOnInit(): void {
    this.displayedColumns = ["slNo","defectType","quantity","operation"];
    this.getDefectReport();
  }

 

  getDefectReport()
  {
    let data =  [
      {
      id: 1,
      defect_type: 'Plugged Cell',
      quantity: '5', 
      },
      {
        id: 2,
        defect_type: 'Missing Lot Mark',
        quantity: '14', 
      }
  ];
    this.dataSource = new MatTableDataSource(data);
  }

  viewDefectDetails(id,element)
  {
    var html = `  <tr>
    <td colspan="5" class="text-center">Data Not Found!!</td> 
    </tr>`;
    $("#defect-details-body").html(html);
    $("#defect-report-table").css({width:"30%"});
    $("#defect-report-table").addClass("table-right-border");
    $(".defect-detail-table-wrap").css({width:"70%"});
    this.displayedColumns = ["slNo","defectTypeNew"];
    this.selectedRowIndex = id;
    $(".defect-detail-table-wrap").removeClass('invisible-element');
    $(id).addClass('invisible-element');
  }



// highlight(row){
//     console.log(row);
//     this.selectedRowIndex = row.id;
// }
  backNormal()
  {
    this.selectedRowIndex = -1;
    $("#defect-report-table").css({width:"100%"});
    $("#defect-report-table").removeClass("table-right-border");
    this.displayedColumns = ["slNo","defectType","quantity","operation"];
    $(".defect-detail-table-wrap").addClass('invisible-element');

  }

  // onDateSelection(date: NgbDate) {
  //   console.log(this.fromDate)

  //   if (!this.fromDate && !this.toDate) {
  //     this.fromDate = date;
  //   } else if (this.fromDate && !this.toDate && date.after(this.fromDate)) {
  //     this.toDate = date;
  //   } else {
  //     this.toDate = null;
  //     this.fromDate = date;
  //   }
  //   console.log(this.toDate)

  // }
  // isHovered(date: NgbDate) {
  //   return this.fromDate && !this.toDate && this.hoveredDate && date.after(this.fromDate) && date.before(this.hoveredDate);
  // }

  // isInside(date: NgbDate) {
  //   return date.after(this.fromDate) && date.before(this.toDate);
  // }

  // isRange(date: NgbDate) {
  //   return date.equals(this.fromDate) || date.equals(this.toDate) || this.isInside(date) || this.isHovered(date);
  // }

}
