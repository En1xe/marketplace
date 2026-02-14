import { Button } from 'antd'
import { MenuOutlined, CloseOutlined } from '@ant-design/icons'

import Logo from '@comps/ui/Logo/Logo'
import BasicLink from '@comps/ui/Links/BasicLink/BasicLink'
import BasicButton from '@comps/ui/Buttons/BasicButton/BasicButton'
import ChatLink from '@comps/ui/Links/ChatLink/ChatLink'
import useAuth from '@hooks/useAuth'


export default function HeaderSideMenu({menuData, isMenuOpen, setIsMenuOpen}) {
    const { userData } = useAuth()

    return (
        <>
            <Button 
                size='large'
                type='text'
                className='text-2xl! relative!'
                onClick={() => setIsMenuOpen(true)}
                icon={<MenuOutlined className='text-(--color-grey-500)!' />} 
            />
            {isMenuOpen && (
                <>
                    <aside
                        className='fixed side-menu bg-white h-screen z-2 top-0 right-0 p-5 min-w-75'
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
                                <BasicLink 
                                    to='/profile/'
                                    size='large' 
                                    type='link'  
                                    className='flex! justify-start! text-(--color-grey-500)'
                                >
                                    <img 
                                        src={userData?.avatar} 
                                        className='w-10 h-10 rounded-full object-cover' 
                                    />
                                    {userData?.username}
                                </BasicLink>
                                <ChatLink 
                                    text='Chat' 
                                    className='flex! justify-start!'
                                />
                                <ul className="flex flex-col gap-3">
                                    {menuData.map(name => (
                                        <li className="" key={name}>
                                            <BasicLink 
                                                className='text-xl! hover:text-(--color-grey-500-hover)! 
                                                flex! active:text-(--color-grey-500-hover)!'
                                            >
                                                {name}
                                            </BasicLink>
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