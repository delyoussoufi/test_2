import {SafeHtml} from '@angular/platform-browser';

class Entity {
  value: string;
  start: number;
  end: number;
  label: string;
  kb_id: string;
  kb_url: string;

}

export class FoundEntities {
  text: string;
  safeText:  SafeHtml;
  entities: Entity[] = [];
}
