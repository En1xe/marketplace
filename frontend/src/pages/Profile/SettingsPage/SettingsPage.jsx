import { Typography, message } from "antd";

import ProfileLayout from "@comps/layout/Layouts/ProfileLayout/ProfileLayout";

import BasicButton from "@comps/ui/Buttons/BasicButton/BasicButton";
import BasicInput from "@comps/ui/Inputs/BasicInput/BasicInput";
import BasicForm from "@comps/ui/Forms/BasicForm/BasicForm";

import useAuth from "@hooks/useAuth";
import useUserFormFields from "@hooks/useUserFormFields";
import useFormData from "@hooks/useForm";

import { usersService } from "@services/api/users.service";


export default function SettingsPage() {
    const { userData } = useAuth()
    const { formFields } = useUserFormFields(userData)
    const {
        formData, 
        setInputChange, 
        setInputOTPChange, 
        setCheckBoxChange, 
        setUploadFilesChange,
        error
    } = useFormData(formFields)

    const onUpdateUserDataFormSubmit = async (e) => {
        e.preventDefault()

        const file = formData['file']

        const formDataForFile = new FormData()
        formDataForFile.append('file', file)

        const formDataForUser = {...formData}
        delete formData.file

        try {
            const response = await usersService.updateUser(userData.uuid, formDataForUser)

            if (response) {
                message.success('User data was successfully updated')
            }
        } catch (error) {
            message.error('User data were not updated')
        }

        try {
            if (!file) return
            const response = await usersService.uploadUserAvatar(userData.uuid, formDataForFile)

            if (response) {
                message.success('Avatar was successfully updated')
            }
        } catch (error) {
            message.error('Avatar was not updated')
        }
    }

    return (
        <ProfileLayout 
            title='Settings'
            breadcrumbItems={[
                {title: 'Settings'}
            ]}
            currPage='Settings'
            userData={userData}
        >
            <div className="flex flex-col gap-10 sm:w-1/2">
                <div className="flex flex-col gap-4">
                    <div className="text-2xl font-medium">Account information</div>
                    <div className="">
                        <BasicForm 
                            error={error}
                            onSubmit={onUpdateUserDataFormSubmit}
                            fields={formFields}
                            formData={formData}
                            setInputChange={setInputChange}
                            setInputOTPChange={setInputOTPChange}
                            setCheckBoxChange={setCheckBoxChange}
                            setUploadFilesChange={setUploadFilesChange}
                            submitButtonText='Confirm changes'
                        />
                    </div>
                </div>
                <div className="flex flex-col gap-6">
                    <div className="flex gap-2 flex-col">
                        <label htmlFor="email">Email</label>
                        <BasicInput
                            className='py-2! px-4!'
                            id='email'
                            value={userData?.email}
                            readOnly
                            suffix={
                                <Typography.Text copyable={{text: userData?.email}} />
                            }
                        />
                        <BasicButton 
                            type='primary'
                            disabled={userData?.is_oauth}
                        >
                            Change email
                        </BasicButton>
                    </div>
                    <div className="flex gap-2 flex-col">
                        <label htmlFor="">Password</label>
                        <BasicButton type='primary'>
                            Change password
                        </BasicButton>
                    </div>
                </div>
            </div>
        </ProfileLayout>
    )
}