import { Vorgang } from './model.vorgang';

export class VorgangTransfer {
    isSelected: boolean;
    isFinished: boolean;
    isLoading: boolean;
    processed: boolean;
    report: string;
    vorgang: Vorgang;
}
