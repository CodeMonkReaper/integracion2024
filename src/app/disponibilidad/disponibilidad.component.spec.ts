import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DisponibilidadComponent } from './disponibilidad.component';

describe('DisponibilidadComponent', () => {
  let component: DisponibilidadComponent;
  let fixture: ComponentFixture<DisponibilidadComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [DisponibilidadComponent]
    });
    fixture = TestBed.createComponent(DisponibilidadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
