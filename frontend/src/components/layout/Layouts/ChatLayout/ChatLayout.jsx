import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { Input } from "antd";

import ProfileLayout from "@comps/layout/Layouts/ProfileLayout/ProfileLayout";

import useAuth from "@hooks/useAuth";

import user_img from '@assets/icons/basic-user-avatar.png'

import { getFormattedChats, getLastMessageTime } from "@utils";

import { chatsService } from "@services/api/chats.service";


export default function ChatLayout({children, title, breadcrumbItems = [], isParticularChat = false}) {
    const {userData} = useAuth()
    const [chats, setChats] = useState([])

    useEffect(() => {
        const fetchChats = async () => {
            if (!userData) return

            try {
                const chats = await chatsService.getChats()

                if (chats) {
                    const formattedChats = getFormattedChats(chats, userData.id)
                    setChats(formattedChats)
                }
            } catch (error) {
                console.log(error)
            }
        }

        fetchChats()
    }, [userData])

    return (
        <ProfileLayout 
            title={title}
            breadcrumbItems={breadcrumbItems}
            currPage='Chats'
            userData={userData}
        >
            <div className="flex gap-4">
                <div className={`flex-col gap-4 w-full lg:max-w-100 ${isParticularChat ? 'hidden' : 'flex'}`}>
                    <div className="text-2xl">Message</div>
                    <Input.Search 
                        className="max-w-100! z-0!"
                        placeholder="Search"
                        allowClear
                        enterButton
                    />
                    <ul className="flex flex-col gap-4 overflow-y-auto h-100 overflow-hidden">
                        {chats.map(({uuid, anotherParticipant, lastMessage, listing}) => (
                            <Link
                                to={`/profile/chats/${uuid}`}
                                key={uuid}
                            >
                                <li 
                                    className="flex flex-col sm:flex-row gap-4 justify-between cursor-pointer hover:bg-(--color-primary-50) 
                                    rounded-lg py-2 px-3"
                                >
                                    <div className="flex flex-col sm:flex-row items-start gap-2 min-w-0">
                                        <img 
                                            src={anotherParticipant?.avatar || user_img} 
                                            alt="User Image" 
                                            width='40'
                                            className="rounded-full" 
                                        />
                                        <div className="min-w-0 flex-1">
                                            <div className="text-xl text-(--color-dark-900) font-medium">
                                                {anotherParticipant?.username}
                                            </div>
                                            <div className="flex gap-1">
                                                <span>{listing.title}</span>
                                                •
                                                <span>
                                                    {listing.is_price_negotiable
                                                        ? 'Neg.'
                                                        : `${listing.price}$`
                                                    }
                                                </span>
                                            </div>
                                            <div 
                                                className="text-(--color-grey-500) truncate"
                                            >
                                                {lastMessage?.text}
                                            </div>
                                        </div>
                                    </div>
                                    <div className="">
                                        <div className="text-(--color-grey-500)">
                                            {getLastMessageTime(lastMessage?.created_at)}
                                        </div>
                                    </div>
                                </li>
                            </Link>
                        ))}
                    </ul>
                </div>
                <div className={`${!isParticularChat ? 'hidden lg:flex' : ''} flex-1`}>
                    {children}
                </div>
            </div>
        </ProfileLayout>
    )
}