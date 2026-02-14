import { useState, useEffect, useCallback } from "react";
import debounce from "lodash/debounce"
import { Table, Input, notification } from "antd";

import { listingsService } from "@services/api/listings.service";

import profileTableColumns from "./ProfileTableColumns";


export default function ProfileTable({initialListings, currentListings = [], setCurrentListings}) {
    const [api, contextHolder] = notification.useNotification()
    const [searchValue, setSearchValue] = useState('')

    const handleDeleteButtonClick = async (listingUuid) => {
        try {
            const response = await listingsService.deleteListing(listingUuid)

            const newCurrentListings = currentListings.filter(({uuid}) => uuid !== listingUuid)
            setCurrentListings(newCurrentListings)

            api.success({
                title: 'Listing was successfully deleted!'
            })
            
        } catch (e) {
            api.error({
                title: "Something went wrong.",
                description: e.message
            })
        }
    }

    useEffect(() => {
        if (!searchValue) {
            setCurrentListings(initialListings)
            return
        }

        debounceListingsFilter()

        return () => debounceListingsFilter.cancel()
    }, [searchValue])

    const debounceListingsFilter = useCallback(
        debounce(() => {
            const filteredListings = initialListings.filter(({title}) => {
                return title.toLowerCase().includes(searchValue.toLowerCase())
            })

            setCurrentListings(filteredListings)
        }, 500),
        []
    )

    return (
        <div className="flex flex-col gap-4">
            {contextHolder}

            <div className="flex gap-4">
                <Input.Search 
                    value={searchValue}
                    onChange={(e) => setSearchValue(e.target.value)}
                    allowClear 
                    enterButton 
                    className="w-100!"
                    placeholder='Search by ads tittle, keyword...' 
                />
            </div>
            <Table 
                columns={profileTableColumns(handleDeleteButtonClick)} 
                dataSource={currentListings} 
                pagination={{
                    pageSize: 10
                }}
                size='large'
                rowKey='uuid'
            />
        </div>
    )
}