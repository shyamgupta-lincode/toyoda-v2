import { TestBed } from '@angular/core/testing';

import { ToyodaOperatorService } from './toyoda-operator.service';

describe('ToyodaOperatorService', () => {
  let service: ToyodaOperatorService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ToyodaOperatorService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
