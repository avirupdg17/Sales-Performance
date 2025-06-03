import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { UserAuthentication } from '../services/user-authentication';

export const authGuard: CanActivateFn = (route, state) => {
  const router=inject(Router);
  const userAuthenticationService = inject(UserAuthentication);
  if (typeof sessionStorage !== 'undefined') {
    const accessToken = sessionStorage.getItem('access_token');
    const userRole = sessionStorage.getItem('sp_role') || '';
    if (accessToken) {
      userAuthenticationService.setAccessDetails(accessToken, userRole);
      return true; // Allow access to the route
    }
  }

  // Redirect to login if no token or sessionStorage is unavailable
  router.navigate(['/login']);
  return false;
};
