import { Routes } from '@angular/router';
import { Home } from './home/home';
import { Terms } from './terms/terms';
import { Contact } from './contact/contact';
import { PrivacyPolicy } from './privacy-policy/privacy-policy';
import { ProductPage } from './product-page/product-page';
import { CollectionPage } from './collection-page/collection-page';
import { CollectionCategory } from './collection-category/collection-category';
import { Blogs } from './blogs/blogs';
import { BlogContent } from './blog-content/blog-content';
import { WishlistPage } from './wishlist-page/wishlist-page';
import { Login } from './login/login';
import { Register } from './register/register';
import { Dashboard } from './dashboard/dashboard';
import { AddressComponent } from './address/address';
import { ForgotPassword } from './forgot-password/forgot-password';
import { ResetPassword } from './reset-password/reset-password';
import { authGuard } from '../guards/auth.guard';
import { adminGuard } from '../guards/admin.guard';
import { CustomizedOrder } from './customized-order/customized-order';
import { TrackOrder } from './track-order/track-order';
import { ReturnRefund } from './return-refund/return-refund';
import { CheckoutComponent } from './checkout/checkout';
import { AdminOrders } from './admin-orders/admin-orders';

export const routes: Routes = [
    { path: '', component: Home },
    { path: 'checkout', component: CheckoutComponent, canActivate: [authGuard] },
    { path: 'contact', component: Contact },
    { path: 'privacy', component: PrivacyPolicy },
    { path: 'terms', component: Terms },
    { path: 'customized-order', component: CustomizedOrder },
    { path: 'track-order', component: TrackOrder },
    { path: 'return-refund', component: ReturnRefund },

    { path: 'account', component: Dashboard, canActivate: [authGuard] },
    { path: 'account/address', component: AddressComponent, canActivate: [authGuard] },
    { path: 'account/login', component: Login },
    { path: 'account/register', component: Register },
    { path: 'account/forgot-password', component: ForgotPassword },
    { path: 'account/reset-password', component: ResetPassword },

    // Store owner dashboard
    { path: 'admin', component: AdminOrders, canActivate: [adminGuard] },

    { path: 'wishlist', component: WishlistPage },

    {
        path: 'blogs',
        children: [
            { path: '', component: Blogs },
            { path: ':route', component: BlogContent },
        ]
    },

    {
        path: 'collections',
        children: [
            { path: '', component: CollectionPage },
            { path: ':route', component: CollectionCategory },
        ]
    },

    {
        path: 'products', 
        children: [
            { path: '', component: CollectionPage },
            { path: ':short', component: ProductPage },
        ]
    },
];
