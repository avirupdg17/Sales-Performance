import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { MaterialModule } from '../material-module/material-module';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.scss'],
  imports:[MaterialModule]
})
export class Navbar {

  constructor(private router:Router) {

    
  }
  logoutUser(){
    console.log('Logging out user');
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('sp_role');
    this.router.navigate(['/login']);
  }
}