import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';

export const authGuard: CanActivateFn = (route, state) => {
  const router=inject(Router);
  if (typeof sessionStorage !== 'undefined') {
    const accessToken = sessionStorage.getItem('access_token');
    if (accessToken) {
      return true; // Allow access to the route
    }
  }

  // Redirect to login if no token or sessionStorage is unavailable
  router.navigate(['/login']);
  return false;
};
