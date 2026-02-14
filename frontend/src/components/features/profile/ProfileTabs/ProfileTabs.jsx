import { useParams } from 'react-router-dom'

import { Tabs, Empty, message } from 'antd'
import ReviewCard from '@comps/features/profile/ReviewCard/ReviewCard'
import ListingCard from '@comps/features/listings/ListingCard/ListingCard'
import BasicForm from '@comps/ui/Forms/BasicForm/BasicForm'

import useAuth from '@hooks/useAuth'
import useFormData from '@hooks/useForm'

import { reviewsService } from '@services/api/reviews.service'

import { REVIEW_FORM_FIELDS } from './ProfileTabs.constants'


export default function ProfileTabs({userData}) {
    const params = useParams()

    const { 
        formData, 
        setInputChange, 
        setInputOTPChange,
        error, 
        setError
    } = useFormData(REVIEW_FORM_FIELDS)
    const { userData: requestUserData } = useAuth()

    const {reviews_as_seller = [], listings = []} = userData || {}

    const recentAds = listings.filter((el) => el.is_active)
    const completedAds = listings.filter((el) => !el.is_active)

    const onPublishReviewFormSubmit = async (e) => {
        e.preventDefault()

        if (!formData.rating) {
            setError('Set the rating!')
        }

        try {   
            const response = await reviewsService.createReview(formData)

            if (response) {
                console.log(response)
            }
        } catch (e) {
            message.error('Review was not created')
        }
    }

    const PROFILE_TABS_PAGES = [
    {
        key: 'recentAds',
        label: 'Active Ads',
        children: recentAds.length > 0 ? (
            <ul className="grid max-[600px]:grid-cols-1 md:grid-cols-3 grid-cols-2 gap-4.5">
                {recentAds.map(data => (
                    <li key={data.id}>
                        <ListingCard 
                            data={data}
                        />
                    </li>
                ))}
            </ul>
        ) : (
            <Empty description='No ads' />
        )
    },
    {
        key: 'completedAds',
        label: 'Completed Ads',
        children: completedAds.length > 0 ? (
            <ul className="grid max-[600px]:grid-cols-1 md:grid-cols-3 grid-cols-2 gap-4.5">
                {completedAds.map(data => (
                    <li key={data.id}>
                        <ListingCard 
                            data={data}
                        />
                    </li>
                ))}
            </ul>
        ) : (
            <Empty description='No ads' />
        )
    },
    {
        key: 'sellerReview',
        label: 'Seller Review',
        children: reviews_as_seller.length > 0 ? (
            <div className="flex flex-col gap-8">
                {reviews_as_seller.map(data => (
                    <ReviewCard 
                        data={data}
                    />
                ))}
            </div>
        ) : (
            <Empty description='No reviews' />
        )
    },
    {
        key: 'writeReview',
        label: 'Write Review',
        children: params.uuid !== requestUserData?.uuid ? (
            <div className="flex flex-col gap-4">
                <BasicForm 
                    error={error}
                    onSubmit={onPublishReviewFormSubmit}
                    formData={formData}
                    fields={REVIEW_FORM_FIELDS}
                    setInputChange={setInputChange}
                    setInputOTPChange={setInputOTPChange}
                    submitButtonText='Publish review'
                />
            </div>
        ) : (
            <Empty description="You can't write a review about yourself" />
        )
    },
    ]

    return (
        <Tabs 
            type='card' 
            defaultValue='recentAds' 
            className='profile-tabs'
            items={PROFILE_TABS_PAGES}
        />
    )
}