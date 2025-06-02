import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AscUser } from './asc-user';

describe('AscUser', () => {
  let component: AscUser;
  let fixture: ComponentFixture<AscUser>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AscUser]
    })
    .compileComponents();

    fixture = TestBed.createComponent(AscUser);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
