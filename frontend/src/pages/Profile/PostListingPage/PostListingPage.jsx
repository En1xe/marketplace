import { useState } from 'react';
import { Result, message } from 'antd';
import { ArrowRightOutlined } from '@ant-design/icons'

import BasicLink from '@comps/ui/Links/BasicLink/BasicLink';
import ProfileLayout from "@comps/layout/Layouts/ProfileLayout/ProfileLayout";
import BasicForm from "@comps/ui/Forms/BasicForm/BasicForm";

import useAuth from "@hooks/useAuth";
import useFormData from "@hooks/useForm";

import { listingsService } from '@services/api/listings.service';

import { POST_LISTING_FORM_FIELDS } from "./PostListingPage.constants";


export default function PostListingPage() {
    const {userData} = useAuth()
    const {
        formData, 
        setInputChange, 
        setInputOTPChange, 
        setCheckBoxChange, 
        setUploadFilesChange,
        getPreparedFormDataForUpload,
        error
    } = useFormData(POST_LISTING_FORM_FIELDS)

    const [listingUuid, setListingUuid] = useState(null)
    const [showSuccessMessage, setShowSuccessMessage] = useState(false)

    const onPostListingFormSubmit = async (e) => {
        e.preventDefault()

        const [preparedFormData, filesUploadFormData] = getPreparedFormDataForUpload(formData)

        try {
            const data = await listingsService.createListing(preparedFormData)
            
            if (data) {
                filesUploadFormData.append('listing_id', data.id)
                const response = await listingsService.createListingMedia(filesUploadFormData)

                if (response) {
                    setShowSuccessMessage(true)
                    setListingUuid(data.uuid)
                }
            }
        } catch (error) {
            const errorMessage = error.response.data.message
            message.error(errorMessage)
            throw new error
        }
    }

    return (
        <ProfileLayout 
            title='Post an ad'
            breadcrumbItems={[
                {title: 'Post an ad'}
            ]}
            currPage='Post a Listing'
            userData={userData}
        >
            <div className="">
                {!showSuccessMessage
                    ?   <BasicForm
                            error={error}
                            onSubmit={onPostListingFormSubmit}
                            fields={POST_LISTING_FORM_FIELDS}
                            formData={formData}
                            setInputChange={setInputChange}
                            setInputOTPChange={setInputOTPChange}
                            setCheckBoxChange={setCheckBoxChange}
                            setUploadFilesChange={setUploadFilesChange}
                            submitButtonText={(
                                <div className='flex gap-2 items-center'>
                                    Post Listing
                                    <ArrowRightOutlined className='text-xl!' />
                                </div>
                            )}
                                submitButtonClassName='w-50!'
                        />
                    :   <Result 
                            status='success'
                            title='Listing was successfully created!'
                            extra={[
                                <BasicLink to={`/listings/${listingUuid}`}>
                                    See listing
                                </BasicLink>
                            ]}
                        />
                }
            </div>
        </ProfileLayout>
    )
}