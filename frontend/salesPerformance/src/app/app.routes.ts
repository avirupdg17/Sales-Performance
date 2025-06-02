import { Routes } from '@angular/router';
import { Login } from './pages/login/login';
import { Dashboard } from './pages/non-admin-pages/dashboard/dashboard';
import { authGuard } from './guards/auth-guard';
import { Home } from './pages/home/home';

export const routes: Routes = [
  { path: 'login', component: Login },
  { path: 'home', 
    component: Home, 
    canActivate: [authGuard],
    children: [
        {
            path: 'user',
            loadChildren: () => import('./pages/non-admin-pages/non-admin-pages-module').then(m => m.NonAdminPagesModule),
        },
        {
            path:'admin',
            loadChildren: () => import('./pages/adminPages/admin-pages-module').then(m => m.AdminPagesModule),
        }
    ]
},
  { path: '**', redirectTo: 'login' } // Redirect any unknown routes to login
];