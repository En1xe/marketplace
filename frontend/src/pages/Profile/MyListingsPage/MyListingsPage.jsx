import ProfileLayout from "@comps/layout/Layouts/ProfileLayout/ProfileLayout";
import ProfileTable from "@comps/features/profile/ProfileTable/ProfileTable";
import ListingStatisticsCard from '@comps/features/listings/ListingStatisticsCard/ListingStatisticsCard'

import useAuth from "@hooks/useAuth";
import useListings from "@hooks/useListings";


export default function MyListingsPage() {
    const { userData } = useAuth()
    const { 
        currentListings, 
        setCurrentListings, 
        initialListings 
    } = useListings(userData?.id)

    return (
        <ProfileLayout 
            title='My ads'
            breadcrumbItems={[
                {title: 'My ads'}
            ]}
            currPage='My listings'
            userData={userData}
        >
            <div className="lg:flex hidden">
                <ProfileTable 
                    initialListings={initialListings}
                    currentListings={currentListings}
                    setCurrentListings={setCurrentListings}
                />
            </div>
            <ul className="lg:hidden grid md:grid-cols-2 gap-6">
                {currentListings.map(data => (
                    <li key={data.uuid}>
                    <ListingStatisticsCard 
                            data={data}
                        /> 
                    </li>
                ))}
            </ul>
        </ProfileLayout>
    )
}