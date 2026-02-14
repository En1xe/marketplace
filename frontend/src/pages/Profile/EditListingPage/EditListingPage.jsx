import { useState } from 'react';
import { useParams } from 'react-router-dom';

import { Button, Result } from 'antd';
import { ArrowRightOutlined, LeftSquareOutlined} from '@ant-design/icons'

import BasicLink from '@comps/ui/Links/BasicLink/BasicLink';
import ProfileLayout from "@comps/layout/Layouts/ProfileLayout/ProfileLayout";
import BasicForm from "@comps/ui/Forms/BasicForm/BasicForm";

import useAuth from "@hooks/useAuth";
import useFormData from "@hooks/useForm";
import { useEditListingFormFields } from '@hooks/useListingFormFields';

import { listingsService } from '@services/api/listings.service';


export default function EditListingPage() {
    const params = useParams()

    const [listingUuid, setListingUuid] = useState(null)
    const [showSuccessMessage, setShowSuccessMessage] = useState(false)

    const { formFields } = useEditListingFormFields(params.uuid)
    const { userData } = useAuth()
    const {
        formData, 
        setInputChange, 
        setInputOTPChange, 
        setCheckBoxChange, 
        setUploadFilesChange,
        getPreparedFormDataForUpload,
        error
    } = useFormData(formFields)

    const onPostListingFormSubmit = async (e) => {
        e.preventDefault()

        const [
            preparedFormData, 
            filesUploadFormData, 
        ] = getPreparedFormDataForUpload(formData)

        try {
            const data = await listingsService.updateListing(params.uuid, preparedFormData)

            if (data) {
                filesUploadFormData.append('listing_id', data.id)

                const response = await listingsService.updateListingMedia(filesUploadFormData)

                if (response) {
                    setShowSuccessMessage(true)
                    setListingUuid(data.uuid)
                }
                    
            }
        } catch (error) {
            console.log(error)
            throw new error
        }
    }

    return (
        <ProfileLayout 
            title='Edit ads'
            breadcrumbItems={[
                {title: 'My ads', href: '/profile/my_listings'},
                {title: 'Edit ads'}
            ]}
            currPage='Edit the listing'
            userData={userData}
        >
            <div className="flex gap-4">
                <BasicLink
                    to='/profile/my_listings' 
                    size='large'
                    icon={<LeftSquareOutlined className='text-2xl!' />}
                />
                <div className="flex-1">
                    {!showSuccessMessage
                        ?   <BasicForm
                                error={error}
                                onSubmit={onPostListingFormSubmit}
                                fields={formFields}
                                formData={formData}
                                setInputChange={setInputChange}
                                setInputOTPChange={setInputOTPChange}
                                setCheckBoxChange={setCheckBoxChange}
                                setUploadFilesChange={setUploadFilesChange}
                                submitButtonText={(
                                    <div className='flex gap-2 items-center'>
                                        Update Listing
                                        <ArrowRightOutlined className='text-xl!' />
                                    </div>
                                )}
                                    submitButtonClassName='w-50!'
                            />
                        :   <Result 
                                status='success'
                                title='Listing was successfully updated!'
                                extra={[
                                    <BasicLink to={`/listings/${listingUuid}`}>
                                        See listing
                                    </BasicLink>
                                ]}
                            />
                    }
                </div>
            </div>
        </ProfileLayout>
    )
}