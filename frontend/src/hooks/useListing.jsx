import { useState, useEffect } from "react";

import { listingsService } from "@services/api/listings.service";

import { useAsyncThrow } from './useAsyncThrow'


export default function useListing(listingUuid) {
    const { setError } = useAsyncThrow()
    const [isLoading, setIsLoading] = useState(true)
    const [listing, setListing] = useState({})

    useEffect(() => {
        const fetchListing = async () => {
            try {
                const listing = await listingsService.getListing(listingUuid)

                if (listing) {
                    setListing(listing)
                    setIsLoading(false)
                }
            } catch (e) {
                setError(e)
            }
        }

        fetchListing()
    }, [])

    return {
        listing,
        isLoading
    }
}