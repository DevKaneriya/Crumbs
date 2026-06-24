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
  if (!req.url.startsWith(environment.apiUrl) || SAFE_METHODS.has(req.method)) {
    return next(req);
  }

  const csrfToken = readCookie('csrftoken');
  if (!csrfToken) {
    return next(req);
  }

  return next(req.clone({ setHeaders: { 'X-CSRFToken': csrfToken } }));
};
