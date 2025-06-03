import { Component, OnInit, signal, Signal } from '@angular/core';
import { Router } from '@angular/router';
import { MaterialModule } from '../material-module/material-module';
import { ApplicationState } from '../../services/application-state';
import { UserAuthentication } from '../../services/user-authentication';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.html',
  styleUrls: ['./navbar.scss'],
  imports:[MaterialModule,CommonModule]
})
export class Navbar implements OnInit {
  hasUserLoggedIn: boolean = false;
  constructor(private router:Router, private applicationStateService:ApplicationState, private userAuthenticationService:UserAuthentication) {

  }
  ngOnInit(): void {
    const userLogged$ = this.userAuthenticationService.hasUserLoggedIn().subscribe({
      next: (response:boolean) => this.hasUserLoggedIn = response,
    });
  }
  logoutUser(){
    this.userAuthenticationService.logOutUser();
    this.router.navigate(['/login']);
  }
  toggleSideNav(){
    this.applicationStateService.toggleSideNav();
  }
}