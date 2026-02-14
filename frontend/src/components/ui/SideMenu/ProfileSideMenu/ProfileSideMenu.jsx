import { Button, Avatar, Divider } from 'antd'
import { CloseOutlined, UnorderedListOutlined } from '@ant-design/icons'

import ProfileLink from '@comps/features/profile/ProfileLink/ProfileLink'
import BasicButton from '@comps/ui/Buttons/BasicButton/BasicButton'

import useAuth from '@hooks/useAuth'

export default function ProfileSideMenu({
    profileLinks,
    isMenuOpen, 
    setIsMenuOpen,
    currPage
}) {
    const { userData } = useAuth()

    return (
        <>
            <Button 
                size='large'
                type='text'
                className='text-2xl! relative!'
                onClick={() => setIsMenuOpen(true)}
                icon={<UnorderedListOutlined className='text-(--color-grey-500)!' />} 
            />
            {isMenuOpen && (
                <>
                    <aside
                        className='fixed side-menu--left bg-white h-screen z-2 top-0 left-0 p-5 min-w-75'
                    >
                        <div className="flex justify-end">
                            <BasicButton
                                size='large'
                                type='text'
                                icon={
                                    <CloseOutlined />
                                }
                                onClick={() => setIsMenuOpen(false)}
                            />
                        </div>
                        <div className='border-[#f0f0f0] rounded-lg w-70'>
                            <div className="flex gap-4 p-8">
                                <Avatar 
                                    src={userData?.avatar} 
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
                                    {profileLinks.map(({text, href, icon}) => (
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
                    </aside>
                    <div className="fixed inset-0 bg-black/60 z-1 backdrop-blur-[2px]" />
                </>
            )}
        </>
    )
}