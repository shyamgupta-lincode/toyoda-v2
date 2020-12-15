import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ToyodaPlanningComponent } from './toyoda-planning.component';

describe('ToyodaPlanningComponent', () => {
  let component: ToyodaPlanningComponent;
  let fixture: ComponentFixture<ToyodaPlanningComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ToyodaPlanningComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ToyodaPlanningComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
