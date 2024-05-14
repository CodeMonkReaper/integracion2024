import { TestBed } from '@angular/core/testing';

import { DivisasService } from './divisas.service';

describe('DivisasService', () => {
  let service: DivisasService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(DivisasService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
