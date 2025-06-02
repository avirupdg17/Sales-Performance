import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Distributor } from './distributor';

describe('Distributor', () => {
  let component: Distributor;
  let fixture: ComponentFixture<Distributor>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Distributor]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Distributor);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
