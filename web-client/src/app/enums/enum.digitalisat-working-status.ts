// This should be equivalent to ClassificationStatus at python's side.
export enum EnumClassificationStatus {
  OPEN = 'Offen',
  CLOSED = 'Abgeschlossen',
  WORKING = 'In Bearbeitung',
}

export type CassificationStatusStrings = keyof typeof EnumClassificationStatus;

export class ClassificationStatusKeyBind {

  public static getWorkingStatusKey(key: CassificationStatusStrings): CassificationStatusStrings {
    return key;
  }
}


