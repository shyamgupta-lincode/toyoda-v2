import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ToyodaOperatorComponent } from './toyoda-operator.component';

describe('ToyodaOperatorComponent', () => {
  let component: ToyodaOperatorComponent;
  let fixture: ComponentFixture<ToyodaOperatorComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ToyodaOperatorComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ToyodaOperatorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
