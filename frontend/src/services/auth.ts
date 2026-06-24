import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, catchError, firstValueFrom, map, of, tap } from 'rxjs';
import { Wishlistservice } from './wishlistservice';
import { Cartservice } from './cartservice';
import { environment } from '../environments/environment';

interface AuthUser {
  id: number;
  first_name: string;
  last_name: string;
  name: string;
  email: string;
  username: string;
}

interface AuthResponse {
  message: string;
  user: AuthUser;
}

interface SessionResponse {
  authenticated: boolean;
  user: AuthUser | null;
}

@Injectable({
  providedIn: 'root'
})
export class Auth {

  private storageKey = 'auth_user';
  private currentUserSubject = new BehaviorSubject<AuthUser | null>(null);
  currentUser$ = this.currentUserSubject.asObservable();
  private initPromise: Promise<void> | null = null;

  constructor(
    private http: HttpClient,
    private wishlistService: Wishlistservice,
    private cartService: Cartservice
  ) {}

  initialize(): Promise<void> {
    if (this.initPromise) {
      return this.initPromise;
    }

    this.initPromise = (async () => {
      if (!this.isBrowser()) {
        return;
      }

      this.initializeCsrfCookie();

      // First try to refresh the access token using the refresh token cookie
      const refreshed = await this.refreshAccessToken();
      
      // Then check the current session
      const session = await this.getSession();
      if (session.authenticated && session.user) {
        this.setCurrentUser(session.user);
        return;
      }

      // If session check failed but we refreshed, try session again
      if (refreshed && !session.authenticated) {
        const refreshedSession = await this.getSession();
        if (refreshedSession.authenticated && refreshedSession.user) {
          this.setCurrentUser(refreshedSession.user);
          return;
        }
      }

      // No valid session - clear everything
      this.clearCurrentUser();
    })();

    return this.initPromise;
  }

  register(data: { first_name: string; last_name: string; email: string; password: string }) {
    return this.http.post<AuthResponse>(
      `${environment.apiUrl}/accounts/register/`,
      data,
      { withCredentials: true }
    ).pipe(
      tap(res => this.setCurrentUser(res.user)),
    );
  }

  login(data: { email: string; password: string }) {
    return this.http.post<AuthResponse>(
      `${environment.apiUrl}/accounts/login/`,
      data,
      { withCredentials: true }
    ).pipe(
      tap(res => this.setCurrentUser(res.user)),
    );
  }

  logout() {
    return this.http.post<{ message: string }>(
      `${environment.apiUrl}/accounts/logout/`,
      {},
      { withCredentials: true }
    ).pipe(
      tap(() => this.clearCurrentUser()),
    );
  }

  user() {
    const currentUser = this.currentUserSubject.value;
    if (currentUser) {
      return of(currentUser);
    }

    // If no current user, try to get fresh session from backend
    return this.http.get<SessionResponse>(
      `${environment.apiUrl}/accounts/session/`,
      { withCredentials: true }
    ).pipe(
      map(res => {
        if (res.authenticated && res.user) {
          this.setCurrentUser(res.user);
          return res.user;
        }
        // Return null if not authenticated
        return null as any;
      }),
      catchError(() => {
        this.clearCurrentUser();
        return of(null as any);
      })
    );
  }

  getToken() {
    return null;
  }

  isLoggedIn() {
    return !!this.currentUserSubject.value;
  }

  isBrowser(): boolean {
    return typeof window !== 'undefined' && !!window.localStorage;
  }

  private loadSavedUser(): AuthUser | null {
    const savedUser = localStorage.getItem(this.storageKey);
    if (!savedUser) {
      return null;
    }

    try {
      return JSON.parse(savedUser) as AuthUser;
    } catch {
      localStorage.removeItem(this.storageKey);
      return null;
    }
  }

  private async getSession(): Promise<SessionResponse> {
    try {
      return await firstValueFrom(
        this.http.get<SessionResponse>(
          `${environment.apiUrl}/accounts/session/`,
          { withCredentials: true }
        ).pipe(
          catchError(() => of({ authenticated: false, user: null }))
        )
      );
    } catch {
      return { authenticated: false, user: null };
    }
  }

  private async refreshAccessToken(): Promise<boolean> {
    try {
      await firstValueFrom(
        this.http.post<{ message: string }>(
          `${environment.apiUrl}/accounts/refresh/`,
          {},
          { withCredentials: true }
        )
      );
      return true;
    } catch {
      return false;
    }
  }

  private initializeCsrfCookie() {
    this.http.get(`${environment.apiUrl}/accounts/csrf/`, { withCredentials: true }).subscribe({
      next: () => undefined,
      error: () => undefined,
    });
  }

  private setCurrentUser(user: AuthUser) {
    this.currentUserSubject.next(user);
    if (this.isBrowser()) {
      localStorage.setItem(this.storageKey, JSON.stringify(user));
    }
  }

  private clearCurrentUser() {
    this.currentUserSubject.next(null);
    if (this.isBrowser()) {
      localStorage.removeItem(this.storageKey);
    }
  }
}
