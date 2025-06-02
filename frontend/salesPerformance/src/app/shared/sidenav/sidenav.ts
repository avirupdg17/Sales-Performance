import { Component } from '@angular/core';
import { MaterialModule } from '../material-module/material-module';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-sidenav',
  templateUrl: './sidenav.html',
  styleUrls: ['./sidenav.scss'],
  imports:[MaterialModule, RouterModule]
})
export class Sidenav {
  sectionsByRole: { [role: string]: { label: string, link: string }[] } = {
    admin: [
      {label:'Upload Data',link:'/home/admin/'},
      { label: 'ASC', link: '/home/admin/asc' },
      { label: 'Distributor', link: '/home/admin/distributor' },
      { label: 'Promoter', link: '/home/admin/promoter' },
      { label: 'XFE', link: '/home/admin/xfe' }
    ],
    user: [
      { label: 'Dashboard', link: '/home/user/dashboard' },
      { label: 'Leaderboard', link: '/home/user/leaderboard' },
      { label: 'User Profile', link: '/home/user/profile' }
    ]
  };
  
  sectionsToShow: { label: string, link: string }[] = [];
  ngOnInit() {
    if (typeof sessionStorage !== 'undefined') {
    const role = sessionStorage?.getItem('sp_role');
    console.log('Role from sessionStorage:', role);
    if (role === 'Admin') {
      this.sectionsToShow = this.sectionsByRole['admin'];
    } else {
      this.sectionsToShow = this.sectionsByRole['user'];
    }
  }
  }
}