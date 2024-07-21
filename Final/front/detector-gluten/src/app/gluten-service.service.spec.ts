import { TestBed } from '@angular/core/testing';

import { GlutenServiceService } from './gluten-service.service';

describe('GlutenServiceService', () => {
  let service: GlutenServiceService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(GlutenServiceService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
