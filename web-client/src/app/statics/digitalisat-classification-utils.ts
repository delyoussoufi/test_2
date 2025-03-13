import {Digitalisat} from '../model/model.digitalisat';
import {ClassificationStatus} from '../model/model.classification-status';
import {SearchCategory} from '../model/model.search-category';

export class DigitalisatClassificationUtils {

  public static getClassificationStatus(digitalisat: Digitalisat, category: SearchCategory): ClassificationStatus {
    if (digitalisat && category) {
      for (const dcs of digitalisat.classificationStatus) {
        if (dcs.searchCategoryId === category.id) {
          return dcs;
        }
      }
    }
    return null;
  }

  public static getClassificationStatusStyle(digitalisat: Digitalisat, category: SearchCategory) {
    const dcs = DigitalisatClassificationUtils.getClassificationStatus(digitalisat, category);
    if (dcs === null) {
      return '';
    }
    if (dcs.status === 'OPEN') {
      return 'fa fa-circle status-idle';
    } else if (dcs.status === 'CLOSED') {
      return 'fa fa-circle status-done';
    } else if (dcs.status === 'WORKING') {
      return 'fa fa-circle status-processing';
    } else {
      return 'fa fa-circle-o status-idle';
    }
  }

  public static getClassificationStatusValue(digitalisat: Digitalisat, category: SearchCategory) {
    const dcs = DigitalisatClassificationUtils.getClassificationStatus(digitalisat, category);
    if (dcs) {
      return dcs.statusValue;
    }
    return '';
  }
}
