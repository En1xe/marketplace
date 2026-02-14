import { useState, useEffect } from 'react';

import { message } from 'antd';

import { listingsService } from '@services/api/listings.service';


export const useEditListingFormFields = (listingUuid) => {
    const [formFields, setFormFields] = useState([])
    
    useEffect(() => {
        if (!listingUuid) return

        const fetchListing = async () => {
            try {
                const listing = await listingsService.getListing(listingUuid)

                if (listing) {
                    const fields = [
                        {
                            name: 'title',
                            type: "text",
                            placeholder: 'List title',
                            label: 'Title',
                            required: true,
                            initialValue: listing.title
                        },
                        {
                            name: 'description',
                            type: "textarea",
                            placeholder: 'List description',
                            label: 'Description',
                            initialValue: listing.description
                        },
                        {
                            name: 'price',
                            type: "price",
                            label: 'Price',
                            defaultValue: 0,
                            required: true,
                            initialValue: listing.price
                        },
                        {
                            name: 'is_price_negotiable',
                            type: "checkbox",
                            label: 'Negotiable',
                            initialValue: listing.is_price_negotiable
                        },
                        {
                            name: 'files',
                            type: 'files',
                            label: 'Upload Files',
                            initialValue: listing.media.map(({uuid, url}) => {
                                return {
                                    uid: uuid,
                                    status: 'done',
                                    url: url
                                }
                            }),
                            required: true, 
                        }
                    ]

                    setFormFields(fields)
                }
            } catch (e) {
                message.error('Listings was not received')
            }
        }

        fetchListing()
    }, [listingUuid])

    return {formFields}
}