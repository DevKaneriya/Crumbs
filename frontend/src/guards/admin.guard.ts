import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { Auth } from '../services/auth';

export const adminGuard: CanActivateFn = async (route, state) => {
  const auth = inject(Auth);
  const router = inject(Router);

  await auth.initialize();

  if (auth.isLoggedIn() && auth.isStaff()) {
    return true;
  }

  // Not logged in → send to login
  if (!auth.isLoggedIn()) {
    router.navigate(['/account/login'], { queryParams: { returnUrl: state.url } });
    return false;
  }

  // Logged in but not staff → back to home
  router.navigate(['/']);
  return false;
};
