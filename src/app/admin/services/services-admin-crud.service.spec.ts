import { TestBed } from '@angular/core/testing';

import { ServicesAdminCrudService } from './services-admin-crud.service';

describe('ServicesAdminCrudService', () => {
  let service: ServicesAdminCrudService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ServicesAdminCrudService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
