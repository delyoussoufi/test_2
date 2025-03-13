import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
    name: 'downloadFile',
    standalone: false
})
export class DownloadFilePipe implements PipeTransform {

  transform(data: Blob, filename: string): string {
    const url = window.URL.createObjectURL(data);

    // create hidden dom element (so it works in all browsers)
    const a = document.createElement('a');
    a.setAttribute('style', 'display:none;');
    document.body.appendChild(a);

    // create file, attach to hidden element and open hidden element
    a.href = url;
    a.download = filename;
    a.click();
    return url;
  }
}
