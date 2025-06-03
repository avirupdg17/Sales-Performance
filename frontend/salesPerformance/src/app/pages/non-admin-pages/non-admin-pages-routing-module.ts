import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { Dashboard } from './dashboard/dashboard';
import { Leaderboard } from './leader-board/leader-board';

const routes: Routes = [
  {
    path: 'dashboard',
    component:Dashboard
  },
  {
    path:'leaderboard',
    component:Leaderboard
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class NonAdminPagesRoutingModule { }
