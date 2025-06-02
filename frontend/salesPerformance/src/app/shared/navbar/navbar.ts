import { Component, signal, Signal } from '@angular/core';
import { Router } from '@angular/router';
import { MaterialModule } from '../material-module/material-module';
import { ApplicationState } from '../../services/application-state';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.scss'],
  imports:[MaterialModule]
})
export class Navbar {
  constructor(private router:Router, private applicationStateService:ApplicationState) {

  }
  logoutUser(){
    console.log('Logging out user');
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('sp_role');
    this.router.navigate(['/login']);
  }
  toggleSideNav(){
    this.applicationStateService.toggleSideNav();
  }
}