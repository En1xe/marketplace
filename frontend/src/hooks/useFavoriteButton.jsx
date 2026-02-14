import { useEffect, useState } from "react"

import { message } from "antd"

import { listingsService } from "@services/api/listings.service"

export const useFavoriteButton = (listingId, userId) => {
    const [isFavoriteButtonActive, setIsFavoriteButtonActive] = useState(false)

    useEffect(() => {
        const fetchListingFavorite = async () => {
            if (!listingId || !userId) return 

            try {
                const response = await listingsService.getListingFavorite({
                    listing_id: listingId
                })

                if (response) {
                    if (response.length > 0) {
                        setIsFavoriteButtonActive(true)
                    }
                }
            } catch (error) {
                console.log(error)
            }
        }

        fetchListingFavorite()
    }, [listingId, userId])

    const onFavoriteButtonClick = async () => {
        if (isFavoriteButtonActive) {
            try {
                const response = await listingsService.deleteListingFavorite(listingId)

                setIsFavoriteButtonActive(false)
            } catch (error) {
                message.error('The listing was not removed from favorite')
            }
        } else {
            try {
                const formData = {
                    listing_id: listingId,
                    user_id: userId
                }

                const response = await listingsService.createListingFavorite(formData)

                setIsFavoriteButtonActive(true)
            } catch (error) {
                message.error('The listing was not added to favorite')
            }
        }
    }

    return {
        isFavoriteButtonActive,
        onFavoriteButtonClick
    }
}