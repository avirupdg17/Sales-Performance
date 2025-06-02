import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AscUser } from './asc-user/asc-user';
import { XfeUser } from './xfe-user/xfe-user';
import { Distributor } from './distributor/distributor';
import { Promoter } from './promoter/promoter';
import { UploadData } from './upload-data/upload-data';

const routes: Routes = [
  {
    path:'asc',
    component:AscUser
  },
  {
    path:'xfe',
    component:XfeUser
  },
  {
    path:'distributor',
    component:Distributor
  },
  {
    path:'promoter',
    component: Promoter
  },
  {
    path: '',
    component:UploadData
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class AdminPagesRoutingModule { }
