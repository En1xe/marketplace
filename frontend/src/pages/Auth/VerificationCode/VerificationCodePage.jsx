import { useParams, useNavigate } from "react-router-dom";

import AuthLayout from '@comps/layout/Layouts/AuthLayout/AuthLayout.jsx'
import AuthBox from '@comps/features/auth/AuthBox/AuthBox'
import BasicForm from "@comps/ui/Forms/BasicForm/BasicForm";

import useForm from "@hooks/useForm";
import useAuth from "@hooks/useAuth";

import { redirectTokenService } from "@services/api/redirectTokens.service";

import { VERIFICATION_CODE_FORM_FIELDS } from "./VerificationCode.constants";


export default function VerificationCodePage() {
    const params = useParams()
    const navigate = useNavigate()

    const {
        formData, 
        setInputChange, 
        setInputOTPChange, 
        error, 
        setError
    } = useForm(VERIFICATION_CODE_FORM_FIELDS)
    const {ConfirmVerificationCode} = useAuth()

    const onSecurityCodeFormSubmit = async (e) => {
        e.preventDefault()

        const code = formData.verifyCode

        const verifyCode = {code}

        try {
            const result = await ConfirmVerificationCode(
                params.uuid,
                verifyCode
            )

            const response = await redirectTokenService.createRedirectToken(verifyCode)

            const token = response.token

            if (result.success) {
                navigate(`new_password?token=${token}`, {replace: true})
            }
        } catch (error) {
            const detail = error.response?.data?.detail     

            if (detail) {
                setError(detail)
            }
            
            setError('invalid code')
        }
    }

    return (
        <AuthLayout
            breadcrumbItems={[
                {title: 'Home'},
                {title: 'Account'},
                {title: 'Security Code'}
            ]}
        >
            <AuthBox
                title='Enter security code'
                form={
                    <BasicForm 
                        error={error}
                        onSubmit={onSecurityCodeFormSubmit}
                        fields={VERIFICATION_CODE_FORM_FIELDS}
                        formData={formData}
                        setInputChange={setInputChange}
                        setInputOTPChange={setInputOTPChange}
                        submitButtonText='Submit'
                    />
                }
            />
        </AuthLayout>
    )
}