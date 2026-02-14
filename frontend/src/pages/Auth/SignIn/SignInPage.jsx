import { useNavigate } from "react-router-dom";

import AuthLayout from '@comps/layout/Layouts/AuthLayout/AuthLayout.jsx'

import BasicLink from '@comps/ui/Links/BasicLink/BasicLink'
import AuthBox from '@comps/features/auth/AuthBox/AuthBox'
import OAuthBox from '@comps/features/auth/OAuthBox/OAuthBox'
import BasicForm from "@comps/ui/Forms/BasicForm/BasicForm";

import useForm from "@hooks/useForm";
import useAuth from "@hooks/useAuth";

import { SIGNIN_FORM_FIELDS } from './SignIn.constants'


export default function SignInPage() {
    const navigate = useNavigate()
    
    const {
        formData, 
        setInputChange, 
        error, 
        setError
    } = useForm(SIGNIN_FORM_FIELDS)
    const { login } = useAuth()

    const onLoginFormSubmit = async (e) => {
        e.preventDefault()

        const userData = {
            email: formData.email,
            password: formData.password
        }

        if (userData.password.length < 6) {
            setError('Password must be at least 6 letters length')
            return
        }

        try {
            const result = await login(userData)
            
            if (result) {
                navigate('/', {replace: true})
            }
        } catch (error) {
            setError('Incorrect email or password')
        }
    }

    return (
        <AuthLayout
            breadcrumbItems={[
                {title: 'Home'},
                {title: 'Account'},
                {title: 'Sign In'}
            ]}
        >
            <AuthBox
                title='Sign In'
                topChildren={
                    <OAuthBox action='Sign In' />
                }
                bottomChildren={
                    <div className="text-center">
                        Don't have an account?&nbsp;
                        <BasicLink 
                            to='/auth/signup' 
                            className='text-(--color-accent)! hover:text-(--color-accent-hover)! inline-block!'
                        >
                            Sign Up
                        </BasicLink>
                    </div>
                }
                form={
                    <BasicForm 
                        error={error}
                        onSubmit={onLoginFormSubmit}
                        formData={formData}
                        fields={SIGNIN_FORM_FIELDS}
                        setInputChange={setInputChange}
                        submitButtonText='Sign In'
                        extraActions={
                            <BasicLink 
                                to='/auth/verify' 
                                className='text-(--color-accent)! hover:text-(--color-accent-hover)!'
                            >
                                Forget password
                            </BasicLink>
                        }
                    />
                }
            />
        </AuthLayout>
    )
}