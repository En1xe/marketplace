import { Button } from 'antd'
import { FilterOutlined, CloseOutlined } from '@ant-design/icons'

import Logo from '@comps/ui/Logo/Logo'
import BasicButton from '@comps/ui/Buttons/BasicButton/BasicButton'
import ListingsFilter from '@comps/features/listings/ListingsFilter/ListingsFilter'


export default function ListingFilterSideMenu({
    initialListings, 
    setCurrentListings, 
    isMenuOpen, 
    setIsMenuOpen
}) {
    return (
        <>
            <Button 
                size='large'
                type='text'
                className='text-2xl! relative!'
                onClick={() => setIsMenuOpen(true)}
                icon={<FilterOutlined className='text-(--color-grey-500)!' />} 
            />
            {isMenuOpen && (
                <>
                    <aside
                        className='fixed side-menu--left bg-white h-screen z-20 top-0 left-0 p-5 min-w-75'
                    >
                        <div className="flex flex-col gap-10">
                            <div className="flex justify-between">
                                <Logo className='flex! justify-start!' />
                                <BasicButton
                                    size='large'
                                    type='text'
                                    icon={
                                        <CloseOutlined />
                                    }
                                    onClick={() => setIsMenuOpen(false)}
                                />
                            </div>
                            <div className="flex flex-col gap-4">
                                <ListingsFilter 
                                    initialListings={initialListings}
                                    setCurrentListings={setCurrentListings}
                                />
                            </div>
                        </div>
                    </aside>
                    <div className="fixed inset-0 bg-black/60 z-10 backdrop-blur-[2px]" />
                </>
            )}
        </>
    )
}