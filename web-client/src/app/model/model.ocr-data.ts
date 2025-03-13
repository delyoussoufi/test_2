
export class Box {
  x0: number;
  y0: number;
  xf: number;
  yf: number;

  constructor({x0, xf, y0, yf}) {
    this.x0 = x0; this.xf = xf; this.y0 = y0; this.yf = yf;
  }

  private area(): number {
    return Math.abs((this.xf - this.x0) * (this.yf - this.y0));
  }

  public isOverlapping(other: Box):  boolean {
    // If one rectangle is on left side of other
    if (this.x0 > other.xf || other.x0 > this.xf) {
      return false;
    }

    // If one rectangle is above other
    return !(this.y0 > other.yf || other.y0 > this.yf);
  }

  public percentOverlappingArea(other: Box) {

    if (!this.isOverlapping(other)) {
      return 0;
    }
    const areaIntersecting = Math.abs((this.xf - other.x0) * (this.y0 - other.yf));
    const smallerArea = Math.min(this.area(), other.area());
    return areaIntersecting / smallerArea;   // compute percent on smaller area.
  }
}

export class Word {
  box: Box;
  confidence: number;
  text: string;
}

export class OcrData {
  words: Array<Word>;
  text: string;
}

export class FoundTerm {
  box: Box;
  value: string;
  score: number;
  score_unit: string;
}

export class SearchTermsFound {
  value: string;
  found_terms: Array<FoundTerm>;
}
