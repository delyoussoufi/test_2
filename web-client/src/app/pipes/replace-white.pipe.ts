import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
    name: 'replaceWhite',
    standalone: false
})
export class ReplaceWhitePipe implements PipeTransform {

  transform(value: string, reg: string): string {
    const re = new RegExp(reg);
    return value?.replace(re, ' ');
  }

}
