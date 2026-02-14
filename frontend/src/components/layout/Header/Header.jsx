import { useState  } from 'react'
import { Layout, Dropdown } from 'antd'
import { 
    PlusCircleOutlined, 
    EyeOutlined, 
    SettingOutlined,
    ProfileOutlined,
} from '@ant-design/icons'

import basicUserAvatar from '@assets/icons/basic-user-avatar.png'

import Logo from '@comps/ui/Logo/Logo'
import BasicLink from '@comps/ui/Links/BasicLink/BasicLink'
import ChatLink from '@comps/ui/Links/ChatLink/ChatLink'
import HeaderSideMenu from '@comps/ui/SideMenu/HeaderSideMenu/HeaderSideMenu'
import BasicButton from '@comps/ui/Buttons/BasicButton/BasicButton'
import SignOutLink from '@comps/ui/Links/SignOutLink/SignOutLink'

import useAuth from '@hooks/useAuth'

import { HOME_PAGE_MENU_NAV } from './Header.constants'


export default function Header() {
    const [isMenuOpen, setIsMenuOpen] = useState(false)
    const { userData } = useAuth()

    const DropDownMenuItems = [
        {
            key: 1,
            label: (
                <BasicLink 
                    to={`/brands/${userData?.uuid}`} 
                    type='link' 
                    className='p-0! text-(--color-black-900)!'
                >
                    <EyeOutlined className='text-xl!' />
                    Public Profile
                </BasicLink>
            )
        },
        {
            key: 2,
            label: (
                <BasicLink 
                    to={`/profile`} 
                    type='link' 
                    className='p-0! text-(--color-black-900)!'
                >
                    <ProfileOutlined className='text-xl!' />
                    Account
                </BasicLink>
            )
        },
        {
            key: 3,
            label: (
                <BasicLink 
                    to={'/profile/settings'} 
                    type='link' 
                    className='p-0! text-(--color-black-900)!'
                >
                    <SettingOutlined className='text-xl!' />
                    Settings
                </BasicLink>
            )
        },
        {
            key: 4,
            label: (
                <SignOutLink />
            )
        },
    ]

    return (
        <Layout.Header 
            className='bg-transparent! h-21! p-0!'
        >
            <div className="container flex items-center justify-between h-full py-4.5">
                <div className="flex h-full items-center">
                    <div className="flex items-center gap-2">
                        <Logo />
                    </div>
                    <div className="hidden lg:block h-8 w-px bg-[#DADDE5] mx-8"></div>
                    <div className="hidden lg:flex lg:gap-2">
                        <ul className="flex xl:gap-8 gap-4">
                            {HOME_PAGE_MENU_NAV.map(name => (
                                <li className="" key={name}>
                                    <BasicLink className='text-(--color-grey-500)! hover:text-(--color-dark-900)!'>
                                        {name}
                                    </BasicLink>
                                </li>
                            ))}
                        </ul>
                    </div>
                </div>
                <div className="hidden lg:flex lg:items-center lg:gap-4 lg:h-full">
                    {userData 
                        ?   <>
                                <ChatLink />
                                
                                <Dropdown trigger={['click']} menu={{items: DropDownMenuItems}}>
                                    <BasicButton type='link'>
                                            <img 
                                                src={userData.avatar || basicUserAvatar} 
                                                className='w-10 h-10 rounded-full object-cover' 
                                            />
                                    </BasicButton>
                                </Dropdown>
                                

                                <BasicLink 
                                    to='/profile/post_listing'
                                    type='primary' 
                                    size='large'
                                    className='bg-(--color-accent)! py-6!
                                            hover:bg-(--color-accent-hover)! px-5!' 
                                    icon={<PlusCircleOutlined />}
                                >
                                    Place an ad
                                </BasicLink>
                            </>
                        :   <BasicLink 
                                to='/auth/signin'
                                type='primary' 
                                size='large'
                                className='text-white! bg-(--color-accent)! 
                                        hover:bg-(--color-accent-hover)! px-5! py-6!' 
                                icon={<PlusCircleOutlined />}
                            >
                                Sign In
                            </BasicLink>
                    }
                </div>
                <div className="lg:hidden flex">
                    <HeaderSideMenu 
                        menuData={HOME_PAGE_MENU_NAV}
                        isMenuOpen={isMenuOpen}
                        setIsMenuOpen={setIsMenuOpen}
                    />
                </div>
            </div>
        </Layout.Header>
    )
}