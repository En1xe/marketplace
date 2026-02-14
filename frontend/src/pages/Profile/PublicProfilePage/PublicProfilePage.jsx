import { useParams } from 'react-router-dom'
import { useEffect, useState } from 'react'

import { Rate, Divider, Card } from 'antd'

import AppLayout from '@comps/layout/Layouts/BasicLayout/Layout'
import ProfileContactInfo from '@comps/features/profile/ProfileContactInfo/ProfileContactInfo'
import ProfileTabs from '@comps/features/profile/ProfileTabs/ProfileTabs.jsx'

import user_img from '@assets/icons/basic-user-avatar.png'

import useAuth from '@hooks/useAuth.jsx'
import { useAsyncThrow } from '@hooks/useAsyncThrow'


export default function PublicProfilePage() {
    const params = useParams()

    const { getUserByUUID } = useAuth()
    const { setError } = useAsyncThrow()

    const [user, setUser] = useState(null)
    

    useEffect(() => {
        const fetchUserData = async () => {
            try {
                const userData = await getUserByUUID(params.uuid, true)
                setUser(userData)
            } catch (e) {
                setError(e)
            }
        }

        fetchUserData()
    }, [])

    return (
        <AppLayout 
            title='Profile'
            breadcrumbItems={[
                {title: 'Home'},
                {title: 'Profile'},
            ]}
        >
            <div className="grid lg:grid-cols-4 gap-10">
                <Card className="">
                    <div className="flex gap-10 max-[760px]:flex-col lg:flex-col lg:gap-0">
                        <div className="flex flex-col items-center min-w-max">
                            <img 
                                className='rounded-full w-22.5 h-22.5 object-cover'
                                src={user?.avatar || user_img} 
                                alt="User avatar"
                            />
                            <div className="flex flex-col gap-1 items-center">
                                <div className="text-(--color-dark-900) font-medium">{user?.username}</div>
                                <div className="flex flex-col gap-0.5 items-center">
                                    <div className="">{user?.rating} Star Rating</div>
                                    {user?.rating !== undefined && 
                                        <Rate 
                                            disabled 
                                            allowHalf 
                                            defaultValue={user.rating} 
                                        />
                                    }
                                </div>
                            </div>
                        </div>
                        <Divider className='lg:block! hidden!' />
                        <div className="flex flex-col gap-2">
                            <div className='uppercase text-(--color-grey-500)'>
                                contact information
                            </div>
                            <div className="">
                                <ProfileContactInfo
                                    email='kevin.gilbert@gmail.com'
                                    address='4517 New York. Manchester, Kentucky 394'
                                />
                            </div>
                        </div>
                        <Divider className='lg:block! hidden!' />
                        <div className="flex flex-col gap-2">
                            <div className='uppercase text-(--color-grey-500)'>
                                seller biography
                            </div>
                            <div className="text-(--color-dark-700)">
                                Cras varius ante vel euismod placerat. Sed mattis orci et interdum volutpat. Phasellus a nulla vel augue ullamcorper lacinia a ut metus.
                            </div>
                        </div>
                    </div>
                </Card>
                <div className="flex flex-col lg:col-span-3 gap-5">
                    <Card>
                        <div className="">
                            <ProfileTabs 
                                userData={user}
                            />
                        </div>
                    </Card>
                </div>
            </div>
        </AppLayout>
    )
}