import { HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthInterceptor implements HttpInterceptor {

  constructor() { }
  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Retrieve the access token from sessionStorage
    const accessToken = sessionStorage.getItem('access_token');
    console.log('Access Token:', accessToken);
    // Clone the request and set the new header in one step
    if (accessToken) {
      const cloned = req.clone({
        headers: req.headers.set('Authorization', `Bearer ${accessToken}`)
      });
      return next.handle(cloned);
    }

    // If no token is found, proceed with the original request
    return next.handle(req);
  }
}
