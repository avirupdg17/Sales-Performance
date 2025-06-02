import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApplicationState {
  private _sideNavOpen:BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  constructor() { }

  toggleSideNav() {
    this._sideNavOpen.next(true);
  }
  sideNavCurrentState(){
    return this._sideNavOpen;
  }
}
