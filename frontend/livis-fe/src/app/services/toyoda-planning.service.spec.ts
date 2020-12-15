import { TestBed } from '@angular/core/testing';

import { ToyodaPlanningService } from './toyoda-planning.service';

describe('ToyodaPlanningService', () => {
  let service: ToyodaPlanningService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ToyodaPlanningService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
