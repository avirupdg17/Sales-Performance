import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UploadData } from './upload-data';

describe('UploadData', () => {
  let component: UploadData;
  let fixture: ComponentFixture<UploadData>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [UploadData]
    })
    .compileComponents();

    fixture = TestBed.createComponent(UploadData);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
