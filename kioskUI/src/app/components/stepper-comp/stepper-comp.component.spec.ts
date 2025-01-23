import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StepperCompComponent } from './stepper-comp.component';

describe('StepperCompComponent', () => {
  let component: StepperCompComponent;
  let fixture: ComponentFixture<StepperCompComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [StepperCompComponent]
    });
    fixture = TestBed.createComponent(StepperCompComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
