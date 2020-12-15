import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { DialogTrainingViewComponent } from './dialog-training-view.component';

describe('DialogTrainingViewComponent', () => {
  let component: DialogTrainingViewComponent;
  let fixture: ComponentFixture<DialogTrainingViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DialogTrainingViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DialogTrainingViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
