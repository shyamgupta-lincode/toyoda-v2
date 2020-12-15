import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'filterByPartNumber',
  pure: false,
})
export class FilterByPartNumberPipe implements PipeTransform {
  transform(items: any[], part_number: any): any {
    if (!items || !part_number) {
      return items;
    }
    // filter items array, items which match and return true will be
    // kept, false will be filtered out
    return items.filter(
      item => item.part_number && item.part_number.toLowerCase().indexOf(part_number.toLowerCase()) !== -1);
  }
}
