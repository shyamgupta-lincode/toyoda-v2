import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ToyodaPartsComponent } from './toyoda-parts.component';

describe('ToyodaPartsComponent', () => {
  let component: ToyodaPartsComponent;
  let fixture: ComponentFixture<ToyodaPartsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ToyodaPartsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ToyodaPartsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
