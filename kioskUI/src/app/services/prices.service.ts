import { Injectable } from '@angular/core';
import { OPERATIONS_PRICES, SETUP_PRICES, ServicePrice } from '../common/models/price.model';

@Injectable({
  providedIn: 'root'
})
export class PricesService {

  constructor() { }

  getSetupPricing(): ServicePrice[] {
    return SETUP_PRICES;
  }

  getOperationPricing(): ServicePrice[] {
    return OPERATIONS_PRICES;
  }
}
