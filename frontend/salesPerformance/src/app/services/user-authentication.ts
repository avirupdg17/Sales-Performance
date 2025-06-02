import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserAuthentication {
  private _accessToken: BehaviorSubject<string> = new BehaviorSubject<string>('');
  private _isUserAuthenticated: BehaviorSubject<{role: string, isAuthenticated: boolean}> = new BehaviorSubject<{role: string, isAuthenticated: boolean}>({role: '', isAuthenticated: false});
  private _isUserLoggedIn: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  private _isUserAdmin: BehaviorSubject<boolean> = new BehaviorSubject<boolean>(false);
  constructor() { }

  setAccessDetails(token: string,role:string) {
    this._accessToken.next(token);
    sessionStorage.setItem('access_token', token);
    sessionStorage.setItem('sp_role', role);
  }
  fetchAccessToken() {
    return this._accessToken;
  }
  fetchUserRole() {
    const role = sessionStorage.getItem('sp_role') || '';
    return role;
  }

}
