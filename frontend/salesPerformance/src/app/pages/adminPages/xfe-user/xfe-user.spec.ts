import { ComponentFixture, TestBed } from '@angular/core/testing';

import { XfeUser } from './xfe-user';

describe('XfeUser', () => {
  let component: XfeUser;
  let fixture: ComponentFixture<XfeUser>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [XfeUser]
    })
    .compileComponents();

    fixture = TestBed.createComponent(XfeUser);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
