import { HttpInterceptorFn } from '@angular/common/http';
import { environment } from '../environments/environment';

const SAFE_METHODS = new Set(['GET', 'HEAD', 'OPTIONS', 'TRACE']);

function readCookie(name: string): string | null {
  if (typeof document === 'undefined') {
    return null;
  }

  const match = document.cookie
    .split('; ')
    .find(cookie => cookie.startsWith(`${name}=`));

  return match ? decodeURIComponent(match.split('=').slice(1).join('=')) : null;
}

export const csrfInterceptor: HttpInterceptorFn = (req, next) => {
  // Only process requests to our API
  if (!req.url.startsWith(environment.apiUrl)) {
    return next(req);
  }

  // Clone request with withCredentials for all API requests
  let clonedReq = req.clone({ withCredentials: true });

  // Add CSRF token for non-safe methods
  if (!SAFE_METHODS.has(req.method)) {
    const csrfToken = readCookie('csrftoken');
    if (csrfToken) {
      clonedReq = clonedReq.clone({ 
        setHeaders: { 'X-CSRFToken': csrfToken }
      });
    }
  }

  return next(clonedReq);
};
