import { useEffect, useState } from "react";

import { Empty } from "antd";

import ProfileLayout from "@comps/layout/Layouts/ProfileLayout/ProfileLayout";
import ListingCard from "@comps/features/listings/ListingCard/ListingCard";

import useAuth from "@hooks/useAuth";

import { listingsService } from "@services/api/listings.service";


export default function FavoriteListingsPage() {
    const {userData} = useAuth()
    const [listingFavorites, setListingFavorites] = useState([])
    
    useEffect(() => {
        if (!userData) return

        const getListingFavorites = async () => {
            try {
                const data = await listingsService.getListingFavorite()

                if (data) {
                    setListingFavorites(data)
                }
            } catch (error) {
                console.log(error)
            }
        }

        getListingFavorites()
    }, [userData])

    return (
        <ProfileLayout 
            title='Favorite ads'
            breadcrumbItems={[
                {title: 'Favorite ads'}
            ]}
            currPage='Favorite'
            userData={userData}
        >
            {listingFavorites.length > 0 
                ?   <ul 
                        className="grid md:grid-cols-2 lg:grid-cols-3 gap-4"
                    >
                        {listingFavorites.map(({id, listing}) => (
                            <ListingCard
                                key={id}
                                data={listing}
                            />
                        ))}
                    </ul>
                :   <div className="flex justify-center items-center h-full">
                        <Empty />
                    </div>
            }
        </ProfileLayout>
    )
}