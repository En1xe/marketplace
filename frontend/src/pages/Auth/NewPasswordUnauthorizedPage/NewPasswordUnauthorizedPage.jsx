import { useNavigate, useParams, useSearchParams } from "react-router-dom";

import AuthLayout from '@comps/layout/Layouts/AuthLayout/AuthLayout.jsx'
import AuthBox from '@comps/features/auth/AuthBox/AuthBox'
import BasicForm from "@comps/ui/Forms/BasicForm/BasicForm";

import useForm from "@hooks/useForm";
import useAuth from "@hooks/useAuth";

import { NEW_PASSWORD_FORM_FIELDS } from './NewPassword.constants'


export default function NewPasswordUnauthorizedPage() {
    const navigate = useNavigate()
    const params = useParams()
    const [searchParams, _] = useSearchParams()

    const {formData, setInputChange, error, setError} = useForm(NEW_PASSWORD_FORM_FIELDS)
    const { updateUserWithinRecovery } = useAuth()

    const onNewPasswordFormSubmit = async (e) => {
        e.preventDefault()
        
        if (formData.password1 !== formData.password2) {
            setError('Passwords don\'t match!')
        }

        const token = searchParams.get('token')
        const verifyCodeUuid = params.uuid

        const data = {
            verify_code_uuid: verifyCodeUuid,
            password: formData.password1,
            token: token
        }

        try {
            const result = await updateUserWithinRecovery(data)

            if (result) {
                navigate('/auth/signin', {replace: true})
            }
        } catch (error) {
            const detail = error.response?.data?.detail
            console.log(error)
            if (detail) {
                setError(detail)
                return
            }

            setError('Some problems happened on the server')
        }
    }

    return (
        <AuthLayout
            breadcrumbItems={[
                {title: 'Home'},
                {title: 'Account'},
                {title: 'Change Password'}
            ]}
        >
            <AuthBox
                title='New password'
                submitBtnText='Confirm password'
                form={
                    <BasicForm 
                        error={error}
                        onSubmit={onNewPasswordFormSubmit}
                        fields={NEW_PASSWORD_FORM_FIELDS}
                        formData={formData}
                        setInputChange={setInputChange}
                        submitButtonText='Submit'
                    />
                }
            />
        </AuthLayout>
    )
}