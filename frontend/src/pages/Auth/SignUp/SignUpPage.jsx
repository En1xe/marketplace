import { useNavigate } from "react-router-dom";

import { Checkbox } from 'antd'

import AuthLayout from '@comps/layout/Layouts/AuthLayout/AuthLayout.jsx'
import BasicLink from '@comps/ui/Links/BasicLink/BasicLink'
import AuthBox from '@comps/features/auth/AuthBox/AuthBox'
import OAuthBox from '@comps/features/auth/OAuthBox/OAuthBox'
import BasicForm from "@comps/ui/Forms/BasicForm/BasicForm";
import useForm from "@hooks/useForm";
import useAuth from "@hooks/useAuth";

import { SIGNUP_FORM_FIELDS } from './SignUp.constants'


export default function SignUpPage() {
    const navigate = useNavigate()
    
    const {
        formData, 
        setInputChange, 
        error, 
        setError
    } = useForm(SIGNUP_FORM_FIELDS)
    const { register } = useAuth()

    const onRegisterFormSubmit = async (e) => {
        e.preventDefault()
        
        if (formData.password1 !== formData.password2) {
            setError('Passwords don\'t match!')
            return
        }

        const userData = {
            name: formData.name,
            surname: formData.surname,
            username: formData.username,
            password: formData.password1,
            email: formData.email
        }

        if (userData.password.length < 6) {
            setError('Password must be at least 6 letters length')
            return
        }

        try {
            const result = await register(userData)
            
            if (result) {
                navigate('/auth/signin', {replace: true})
            }
        } catch (error) {
            const detail = error.response.data?.message
            if (detail) {
                setError(String(detail))
            }
        }
    }

    return (
        <AuthLayout
            breadcrumbItems={[
                {title: 'Home'},
                {title: 'Account'},
                {title: 'Sign Up'}
            ]}
        >
            <AuthBox
                title='Sign Up'
                topChildren={
                    <OAuthBox action='Sign Up' />
                }
                form={
                    <BasicForm 
                        error={error}
                        onSubmit={onRegisterFormSubmit}
                        formData={formData}
                        fields={SIGNUP_FORM_FIELDS}
                        setInputChange={setInputChange}
                        submitButtonText='Sign Up'
                        extraActions={
                            <Checkbox>
                                I've read and agree with your&nbsp;
                                <BasicLink>Privacy Policy</BasicLink> and&nbsp; 
                                <BasicLink>Terms & Conditions</BasicLink>
                            </Checkbox>
                        }
                    />
                }
            />
        </AuthLayout>
    )
}