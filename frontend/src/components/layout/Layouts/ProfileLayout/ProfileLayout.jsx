import { Divider, Card, Avatar } from 'antd'

import AppLayout from '@comps/layout/Layouts/BasicLayout/Layout'
import ProfileLink from '@comps/features/profile/ProfileLink/ProfileLink'
import ProfileSideMenu from '@comps/ui/SideMenu/ProfileSideMenu/ProfileSideMenu'

import { PROFILE_LAYOUT_LINKS } from './ProfileLayout.constants'
import { useState } from 'react'

import useAuth from '@hooks/useAuth'


export default function ProfileLayout({
    currPage, 
    children, 
    title, 
    breadcrumbItems=[]
}) {
    const { userData } = useAuth()

    const [isMenuOpen, setIsMenuOpen] = useState(false)

    return (
        <AppLayout
            title={title}
            breadcrumbItems={[
                {title: 'Home'},
                {title: 'Account'},
                ...breadcrumbItems
            ]}
        >
            <div className="flex gap-4 sm:gap-10">
                <div className="lg:hidden">
                    <ProfileSideMenu 
                        currPage={currPage}
                        profileLinks={PROFILE_LAYOUT_LINKS}
                        isMenuOpen={isMenuOpen}
                        setIsMenuOpen={setIsMenuOpen}
                    />
                </div>
                <div className='border border-0.5 border-solid border-[#f0f0f0] rounded-lg w-70 lg:block hidden'>
                    <div className="flex gap-4 p-8">
                        <Avatar 
                            src={userData?.avatar || null} 
                            className='w-16! h-16!'
                        />
                        <div className="flex flex-col gap-2">
                            <div className="text-xl font-medium">{userData?.username}</div>
                            <div className={`text-${userData?.is_admin ? '(--color-accent)' : '(--color-grey-500)'}`}>
                                {userData?.is_admin ? 'Admin' : 'Member'}
                            </div>
                        </div>
                    </div>
                    <Divider />
                    <div className="flex flex-col gap-4">
                        <ul>
                            {PROFILE_LAYOUT_LINKS.map(({text, href, icon}) => (
                                <li key={text}>
                                    <ProfileLink
                                        is_active={currPage === text}
                                        to={href}
                                    >
                                        <div className="flex gap-2">
                                            {icon}
                                            {text}
                                        </div>
                                    </ProfileLink>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
                <Card className="flex-1">
                    {children}
                </Card>
            </div>
        </AppLayout>
    )
}