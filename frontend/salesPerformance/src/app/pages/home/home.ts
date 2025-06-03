import { Component, OnDestroy, OnInit } from '@angular/core';
import { MaterialModule } from '../../shared/material-module/material-module';
import { Sidenav } from '../../shared/sidenav/sidenav';
import { RouterOutlet } from '@angular/router';
import { ApplicationState } from '../../services/application-state';
import { Subscription } from 'rxjs';
import { BreakpointObserver, Breakpoints } from '@angular/cdk/layout';

@Component({
  selector: 'app-home',
  imports: [MaterialModule,Sidenav,RouterOutlet],
  templateUrl: './home.html',
  styleUrl: './home.scss'
})
export class Home implements OnInit,OnDestroy {
  isSideNavOpen: boolean = false;
  drawerMode: 'side' | 'over' = 'side'; // Default mode for larger screens
  private subscription:Subscription = new Subscription();
  constructor(private applicationStateService: ApplicationState, private breakpointObserver: BreakpointObserver) {
  }
  ngOnInit(): void {
    const toggle$ = this.applicationStateService.sideNavCurrentState( ).subscribe({
      next:(response:boolean) => {this.isSideNavOpen = !this.isSideNavOpen;},
    });
    this.subscription.add(toggle$);
    const observe$ = this.breakpointObserver.observe([Breakpoints.Small, Breakpoints.XSmall]).subscribe(result => {
      if (result.matches) {
        this.drawerMode = 'over'; // Use 'over' mode for small screens
        this.isSideNavOpen = false; // Close side nav on small screens
      } else {
        this.drawerMode = 'side'; // Use 'side' mode for larger screens
        this.isSideNavOpen = true; 
      }
    });
    this.subscription.add(observe$);
  }

  ngOnDestroy(): void {
    this.subscription.unsubscribe();
  }
}
