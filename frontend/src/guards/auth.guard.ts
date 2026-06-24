import { inject } from '@angular/core';
import { Router, CanActivateFn } from '@angular/router';
import { Auth } from '../services/auth';

export const authGuard: CanActivateFn = async (route, state) => {
  const auth = inject(Auth);
  const router = inject(Router);

  // Wait for auth initialization to complete
  await auth.initialize();

  // Check if user is logged in after initialization
  if (auth.isLoggedIn()) {
    return true;
  }

  // If not logged in, redirect to login with return URL
  router.navigate(['/account/login'], {
    queryParams: { returnUrl: state.url }
  });
  
  return false;
};
