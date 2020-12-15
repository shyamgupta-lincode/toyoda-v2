import { TestBed } from '@angular/core/testing';

import { ToyodaPartService } from './toyoda-part.service';

describe('ToyodaPartService', () => {
  let service: ToyodaPartService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ToyodaPartService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
