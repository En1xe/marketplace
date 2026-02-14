import { useState, useEffect } from "react";

import { listingsService } from "@services/api/listings.service";


export default function useListings(publisherId, activeOnly=false) {
    const [isLoading, setIsLoading] = useState(true)
    const [currentListings, setCurrentListings] = useState([])
    const [initialListings, setInitialListings] = useState([])

    useEffect(() => {
        const fetchListings = async () => {
            if (!publisherId) {
                setCurrentListings([])
                setInitialListings([])
                return 
            }

            let filters = {}

            if (activeOnly) {
                filters.is_active = activeOnly
            }

            if (publisherId !== 'all') {
                filters.publisher_id = publisherId
            }   

            let data = await listingsService.getListings(filters)

            if (data) {
                data = data.map((listing) => {
                    const date = new Date(listing.created_at)
                    const formattedData = new Intl.DateTimeFormat(
                        'en-EN', 
                        {
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric',
                        }
                    ).format(date)

                    return {
                        key: `listing-${listing.uuid}`,
                        uuid: listing.uuid,
                        title: listing.title,
                        createdAt: formattedData,
                        price: listing.price.toFixed(2),
                        media: listing.media,
                        is_active: listing.is_active,
                    }
                })
                setCurrentListings(data)
                setInitialListings(data)
                setIsLoading(false)
            }
        }

        fetchListings()
    }, [publisherId])

    return {
        currentListings,
        setCurrentListings,
        initialListings,
        setInitialListings,
        isLoading
    }
}