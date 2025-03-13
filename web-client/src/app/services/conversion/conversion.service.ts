import { Injectable } from '@angular/core';

@Injectable()
export class ConversionService {

  constructor() { }

  public convertDateToGermanDateString(date: any) {
    let day: number;
    let month: number;
    let year: number;
    if (date instanceof Date) {
      day = date.getDate();
      month = date.getMonth() + 1;
      year = date.getFullYear();
    }
    if (date && date.day && date.month && date.year) {
      day = date.day;
      month = date.month;
      year = date.year;
    }
    if (day && month && year) {
      return (day <= 9 ? '0' + day : '' + day) + '.'
        + (month <= 9 ? '0' + month : '' + month) + '.'
        + year;
    }
    return null;
  }

  public convertGermanDateStringToDate(dateString: string): Date {
    if (dateString) {
      const parts: Array<string> = dateString.match(/(\d+)/g);
      return new Date(parseInt(parts[2], 10), parseInt(parts[1], 10) - 1, parseInt(parts[0], 10));
    }
    return null;
  }

  public convertTimeStringToDate(timeString: string): Date {
    if (timeString) {
      const parts: Array<string> = timeString.match(/(\d+)/g);
      const date = new Date();
      date.setHours(parseInt(parts[0], 10));
      date.setMinutes(parseInt(parts[1], 10));
      date.setSeconds(parseInt(parts[2], 10));
      return date;
    }
    return null;
  }

  public convertDateTimeToDate(dateWithTime: Date): Date {
    if (dateWithTime) {
      const date = new Date(dateWithTime);
      date.setHours(0, 0, 0, 0);
      return date;
    }
    return null;
  }

  public printDatepickerModel(input: any): string {
    if (input && input.day && input.month && input.year) {
      return input.day + '.' + input.month + '.' + input.year;
    }
    return null;
  }

  public printTimeFromDate(date: Date): string {
    if (date) {
      const hours = date.getHours();
      const minutes = date.getMinutes();
      return hours + ':' + (minutes <= 9 ? '0' + minutes : '' + minutes);
    }
    return null;
  }

  public adaptTimeZone(date: Date) {
    if (date) {
      const hoursDiff = date.getHours() - date.getTimezoneOffset() / 60;
      // const minutesDiff = (date.getHours() - date.getTimezoneOffset()) % 60;
      date.setHours(hoursDiff);
      // date.setMinutes(minutesDiff);
      return date;
    }
    return date;
  }

}
