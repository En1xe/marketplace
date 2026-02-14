import { useState } from 'react'

import { Select } from 'antd'

import ListingCard from '@comps/features/listings/ListingCard/ListingCard'
import AppLayout from '@comps/layout/Layouts/BasicLayout/Layout'
import ListingsFilter from '@comps/features/listings/ListingsFilter/ListingsFilter'
import ListingFilterSideMenu from '@comps/ui/SideMenu/ListingFilterSideMenu/ListingFilterSideMenu' 

import useListings from '@hooks/useListings'


export default function SearchListingsPage() {
    const {
        isLoading,
        currentListings, 
        setCurrentListings, 
        initialListings
    } = useListings('all', true)
    
    const [ isMenuOpen, setIsMenuOpen ] = useState(false)

    return (
        <AppLayout 
            title='Ad List'
            breadcrumbItems={[
                {title: 'Home'},
                {title: 'Ad List'}
            ]}
        >
            <div className="flex flex-col gap-4">
                <div className="flex justify-between gap-4">
                    <div className="text-2xl py-6 text-(--color-grey-500)">
                        <span className='font-medium text-(--color-dark-900)'>
                            {currentListings?.length}
                        </span>&nbsp;
                        <span className="span">Results Found</span>
                    </div>
                    <div className="flex gap-4 items-center">
                        <Select
                            placeholder='Sort By'
                            className='min-w-40'
                            allowClear
                            options={[
                                {value: 'desc', label: 'Minimum Price'},
                                {value: 'asc', label: 'Maximum Price'},
                                {value: 'recent', label: 'Release date'},
                            ]}
                        />
                    </div>
                </div>
                <div className="lg:hidden flex">
                    <ListingFilterSideMenu 
                        initialListings={initialListings}
                        setCurrentListings={setCurrentListings}
                        isMenuOpen={isMenuOpen}
                        setIsMenuOpen={setIsMenuOpen}
                    />
                </div>
                <div className="grid lg:grid-cols-4 py-4 gap-6">
                    <div className="hidden lg:block">
                        <ListingsFilter 
                            initialListings={initialListings}
                            setCurrentListings={setCurrentListings}
                        />
                    </div>
                    <div className="col-span-3">
                        <ul className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {isLoading
                                ? Array(9).fill(0).map((_, index) => (
                                    <li key={index}>    
                                        <ListingCard 
                                            isLoading={isLoading}
                                            data={null}
                                        />
                                    </li>
                                ))
                                
                                : currentListings?.map(data => (
                                <li key={data.uuid}>
                                    <ListingCard 
                                        isLoading={isLoading}
                                        data={data}
                                    />
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
            </div>
        </AppLayout>
    )
}