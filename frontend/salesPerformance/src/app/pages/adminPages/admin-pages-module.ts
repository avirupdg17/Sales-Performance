import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { AdminPagesRoutingModule } from './admin-pages-routing-module';
import { MaterialModule } from '../../shared/material-module/material-module';
import { UploadData } from './upload-data/upload-data';


@NgModule({
  declarations: [
  ],
  imports: [
    CommonModule,
    AdminPagesRoutingModule,
  ]
})
export class AdminPagesModule { }
