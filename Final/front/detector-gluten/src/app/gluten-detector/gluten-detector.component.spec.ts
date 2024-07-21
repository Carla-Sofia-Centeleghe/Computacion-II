import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GlutenDetectorComponent } from './gluten-detector.component';

describe('GlutenDetectorComponent', () => {
  let component: GlutenDetectorComponent;
  let fixture: ComponentFixture<GlutenDetectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GlutenDetectorComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GlutenDetectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
function expect(component: GlutenDetectorComponent) {
  throw new Error('Function not implemented.');
}

