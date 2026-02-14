import { useNavigate } from "react-router-dom";

import AuthLayout from '@comps/layout/Layouts/AuthLayout/AuthLayout.jsx'
import AuthBox from '@comps/features/auth/AuthBox/AuthBox'
import BasicForm from "@comps/ui/Forms/BasicForm/BasicForm";

import useForm from "@hooks/useForm";
import useAuth from "@hooks/useAuth";

import { EMAIL_RECOVERY_FORM_FIELDS } from './EmailRecovery.constants'


export default function EmailRecoveryPage() {
    const navigate = useNavigate()

    const {
        formData, 
        setInputChange, 
        error, 
        setError
    } = useForm(EMAIL_RECOVERY_FORM_FIELDS)
    const { getUserByEmail, createVerificationCode } = useAuth()

    const onEmailRecoveryFormSubmit = async (e) => {
        e.preventDefault()

        try {
            const email = formData.email
            const user = await getUserByEmail(email)
            
            if (!user) {
               setError('User wasn\'t found')
            }
            
            const verificationCodeData = {
                user_id: user.id,
                email: formData.email,
                operation_type: 'change_password',
                field_value: ''
            }

            try {
                const verificationCode = await createVerificationCode(verificationCodeData)

                if (verificationCode) {
                    navigate(`/auth/verify/${verificationCode.uuid}`, {replace: true})
                }
            } catch (error) {
                console.log(error)
                setError('Some problems happened on the server')
            }

        } catch (error) {
            const detail = error.response?.data?.detail
            if (detail) {
                setError(detail)
            }
        }
    }

    return (
        <AuthLayout
            breadcrumbItems={[
                {title: 'Home'},
                {title: 'Account'},
                {title: 'Email Recovery'}
            ]}
        >
            <AuthBox
                title='Password Recovery'
                submitBtnText='Recover password'
                form={
                    <BasicForm 
                        error={error}
                        onSubmit={onEmailRecoveryFormSubmit}
                        fields={EMAIL_RECOVERY_FORM_FIELDS}
                        formData={formData}
                        setInputChange={setInputChange}
                        submitButtonText='Submit'
                    />
                }
            />
        </AuthLayout>
    )
}