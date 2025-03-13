import { Pipe, PipeTransform } from '@angular/core';
import {DomSanitizer, SafeUrl} from '@angular/platform-browser';

@Pipe({
    name: 'blobToSafeUrl',
    standalone: false
})
export class BlobToSafeUrlPipe implements PipeTransform {

  constructor(protected sanitizer: DomSanitizer) {}

  transform(data: Blob): SafeUrl {
    if (data) {
      return this.sanitizer.bypassSecurityTrustUrl(URL.createObjectURL(data));
    }
    return null;
  }
}
