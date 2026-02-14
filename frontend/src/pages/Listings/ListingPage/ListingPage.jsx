import { useEffect } from 'react'
import { useParams } from 'react-router-dom'

import { Carousel, Typography, Statistic, Image, Divider, Skeleton } from 'antd'

import FavoriteButton from '@comps/ui/Buttons/FavoriteButton/FavoriteButton'
import BasicLink from '@comps/ui/Links/BasicLink/BasicLink'
import AppLayout from '@comps/layout/Layouts/BasicLayout/Layout'
import ProfileContactInfo from '@comps/features/profile/ProfileContactInfo/ProfileContactInfo'
import SendMessageButton from '@comps/ui/Buttons/SendMessageButton/SendMessageButton'
import SendEmailButton from '@comps/ui/Buttons/SendEmailButton/SendEmailButton'

import user_img from '@assets/icons/basic-user-avatar.png'

import { getFormattedDataFromString } from '@utils'

import { useFavoriteButton } from '@hooks/useFavoriteButton'
import useAuth from '@hooks/useAuth'
import useListing from '@hooks/useListing'

import { listingsService } from '@services/api/listings.service'


export default function ListingPage() {
    const params = useParams()

    const {listing, isLoading} = useListing(params.uuid)
    const { userData } = useAuth()
    const {isFavoriteButtonActive, onFavoriteButtonClick} = useFavoriteButton(
        listing?.id,
        userData?.id
    )

    useEffect(() => {
        if (!listing || Object.keys(listing).length === 0) return
        if (!userData || Object.keys(userData).length === 0) return

        if (listing.viewers_id?.includes(userData.id)) return

        const createListingView = async () => {
            try {
                const formData = {
                    listing_id: listing.id
                }

                const response = await listingsService.createListingView(formData)
                
                if (response) {
                    console.log('!!!')
                }
            } catch (e) {
                console.log(e)
            }
        }

        createListingView()
    }, [listing, userData])

    return (
        <AppLayout 
            title='Ad List'
            breadcrumbItems={[
                {title: 'Home'},
                {title: 'Ad List', href: '/listings'},
                {title: 'Item'}
            ]}
        >
            <div className="grid grid-cols-[1fr_max-content] max-[850px]:grid-cols-1 gap-10">
                <div className="flex flex-col gap-10 min-[850px]:w-full">
                    <div className="">
                        <Typography.Title
                            className={`${!listing?.is_active ? 'text-(--color-grey-500)!' : ''}`}
                        >
                            {isLoading ? <Skeleton active paragraph={{rows: 0}} /> : listing.title}
                        </Typography.Title>
                        <div className="flex gap-8">
                            <Statistic 
                                title='Location' 
                                value='Location' 
                            />
                            <Statistic 
                                title='Publication Date' 
                                value={getFormattedDataFromString(listing.created_at)} 
                            />
                            <Statistic 
                                title='Viewers'
                                value={listing?.viewers_id?.length} 
                            />
                        </div>
                    </div>
                    {!isLoading && !listing?.is_active && 
                        <div className='font-medium text-xl bg-yellow-100 py-4 text-center'>
                            The ad has been removed from publication.
                        </div>
                    }
                    <div className="">
                        {isLoading
                            ?   <div className="flex flex-col">
                                    <Skeleton.Node active style={{ width: '100%', height: 600 }} />
                                </div>
                            : <Carousel 
                                arrows
                                className='lg:w-150 max-[1000px]:w-100 max-[500px]:w-75'
                                autoplay={false}
                                effect='fade'
                            >
                                {listing.media?.map(({id, url}) => (
                                    <div className="" key={id}>
                                        <Image
                                            src={url}
                                            width='100%'
                                            height='100%'
                                        />
                                    </div>
                                ))}
                            </Carousel>
                            
                        }
                    </div>
                    <div className="">
                        <Typography.Title level={5}>
                            Description
                        </Typography.Title>
                        {isLoading ? <Skeleton active paragraph={{rows: 2}} /> : listing.description}
                    </div>
                </div>
                <div className="flex flex-col gap-2">
                    <div className="flex items-center justify-between gap-4 text-5xl font-medium">
                        <span>
                            {isLoading
                                ?   <Skeleton active paragraph={{rows: 1}} />
                                : (
                                    listing.is_price_negotiable 
                                        ? 'Price negotiable'
                                        : `${listing.price} $`
                                    
                                )
                            }
                            
                        </span>
                        <FavoriteButton 
                            isActive={isFavoriteButtonActive}
                            onClick={onFavoriteButtonClick}
                            isDisabled={listing?.publisher?.id === userData?.id}
                        />
                    </div>
                    <Divider />
                    {listing?.is_active &&
                        <>
                            <div className="flex flex-col gap-4">
                                <SendMessageButton listing={listing} />
                                <SendEmailButton />
                            </div>
                            <Divider />
                        </>
                    }
                    <div className="flex flex-col gap-8">
                        <div className="flex justify-between">
                            <div className="flex gap-4">
                                {isLoading ? (
                                    <Skeleton.Avatar active size='large' />
                                    ) : (
                                    <img 
                                        className='rounded-full object-cover'
                                        src={listing.publisher?.avatar || user_img} 
                                        alt="User" 
                                        width={56}
                                    />
                                )}
                                <div className="">
                                    <div className="text-(--color-grey-500)">
                                        Added by:
                                    </div>
                                    <div className="text-(--color-dark-900) text-xl font-medium">
                                        {isLoading ? (
                                            <Skeleton active paragraph={{rows: 0}} />
                                        ) : (
                                            listing.publisher?.username
                                        )}
                                    </div>
                                </div>
                            </div>
                            {isLoading ? (
                                <Skeleton.Button active />
                            ) : (
                                <BasicLink 
                                    to={`/brands/${listing.publisher?.uuid}`}
                                >
                                    View Profile
                                </BasicLink>
                            )}
                        </div>
                        <div className="">
                            <ProfileContactInfo
                                email='kevin.gilbert@gmail.com'
                                address='4517 New York. Manchester, Kentucky 394'
                            />
                        </div>
                    </div>
                    <Divider />
                </div>
            </div>
        </AppLayout>
    )
}