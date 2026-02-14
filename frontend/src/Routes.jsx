import { lazy } from 'react'
import {Route, Routes, Navigate} from 'react-router-dom'

import ProtectedAuthLayout from '@comps/routes/ProtectedAuth/ProtectedAuthLayout'

const SignInPage = lazy(() => import("@pages/Auth/SignIn/SignInPage"))
const SignUpPage = lazy(() => import("@pages/Auth/SignUp/SignUpPage"))
const NewPasswordUnauthorizedPage = lazy(() => import("@pages/Auth/NewPasswordUnauthorizedPage/NewPasswordUnauthorizedPage"))
const VerificationCodePage = lazy(() => import("@pages/Auth/VerificationCode/VerificationCodePage"))
const EmailRecoveryPage = lazy(() => import("@pages/Auth/EmailRecovery/EmailRecovery"))
const GithubComplete = lazy(() => import("@pages/Auth/GithubComplete"))
const LogoutPage = lazy (() => import('@pages/Auth/Logout/Logout'))

const SearchListingsPage = lazy(() => import('@pages/Listings/SearchListingsPage/SearchListingsPage'))
const ListingPage = lazy(() => import('@pages/Listings/ListingPage/ListingPage'))

const PublicProfilePage = lazy (() => import('@pages/Profile/PublicProfilePage/PublicProfilePage'))
const PostListingPage = lazy (() => import('@pages/Profile/PostListingPage/PostListingPage'))
const FavoriteListingsPage = lazy (() => import('@pages/Profile/FavoriteListingsPage/FavoriteListingsPage'))
const MyListingsPage = lazy (() => import('@pages/Profile/MyListingsPage/MyListingsPage'))
const SettingsPage = lazy (() => import('@pages/Profile/SettingsPage/SettingsPage'))
const EditListingPage = lazy (() => import('@pages/Profile/EditListingPage/EditListingPage'))
const ChatsPage = lazy (() => import('@pages/Profile/ChatsPage/ChatsPage'))
const ChatPage = lazy (() => import('@pages/Profile/ChatPage/ChatPage'))

const NotFoundPage = lazy(() => import('@pages/Errors/NotFoundPage'))


export const AppRoutes = () => {
    return (
        <Routes>
            <Route path='/' element={<SearchListingsPage />} />
            <Route path='brands/:uuid' element={<PublicProfilePage />} />
            <Route path='profile' element={<ProtectedAuthLayout />}>
                <Route index element={<PostListingPage />} />
                <Route path='post_listing' element={<PostListingPage />} />
                <Route path='edit_listing/:uuid' element={<EditListingPage />} />
                <Route path='chats' element={<ChatsPage />} />
                <Route path='chats/:uuid' element={<ChatPage />} />
                <Route path='favorite' element={<FavoriteListingsPage />} />
                <Route path='my_listings' element={<MyListingsPage />} />
                <Route path='settings' element={<SettingsPage />} />
            </Route>
            <Route path='listings'>
                <Route path=':uuid' element={<ListingPage />} />
            </Route>
            <Route path='auth'>
                <Route index element={<Navigate to='/auth/signin' replace />} />
                <Route path="signin" element={<SignInPage />} />
                <Route path="signup" element={<SignUpPage />} />
                <Route path="verify/:uuid/new_password" element={<NewPasswordUnauthorizedPage />} />
                <Route path="verify/:uuid" element={<VerificationCodePage />} />
                <Route path="verify" element={<EmailRecoveryPage />} />
                <Route path="signout" element={<LogoutPage />} />
            </Route>
            <Route path='oauth'>
                <Route path='github/complete' element={<GithubComplete />} />
            </Route>
            <Route path="*" element={<NotFoundPage />} />
        </Routes>
    )
}