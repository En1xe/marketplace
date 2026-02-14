import { useParams } from "react-router-dom";

import { Card, Popconfirm, Button } from "antd";
import { 
    DeleteOutlined,  
    QuestionCircleOutlined, 
    ArrowLeftOutlined
} from "@ant-design/icons";

import ChatLayout from "@comps/layout/Layouts/ChatLayout/ChatLayout";
import ChatMessagesGroup from "@comps/features/chats/ChatMessagesGroup/ChatMessagesGroup";
import BasicLink from "@comps/ui/Links/BasicLink/BasicLink";
import ChatTextarea from "@comps/features/chats/ChatTextArea/ChatTextArea";

import useChat from "@hooks/useChat";
import useAuth from "@hooks/useAuth";

import { chatMessagesService } from "@services/api/chatMessages.service";

import { getFormattedChatMessages } from "@utils";


export default function ChatPage() {
    const params = useParams()

    const { userData } = useAuth()
    const {
        chat, 
        sendMessage,
        onDeleteChatButtonClick,
        onDeleteChatMessageButtonClick,
    } = useChat(userData, params.uuid)

    const onSendMessageSubmit = async (text) => {
        const formData = {
            chat_id: chat.id,
            text,
        }

        try {
            const data = await chatMessagesService.createChatMessage(formData)

            if (data) {
                sendMessage(data)
            }
        } catch (error) {
            console.log(error)
        }
    }

    const messagesByDates = getFormattedChatMessages(
        chat?.messages || [], 
        chat?.currentParticipant, 
        chat?.anotherParticipant
    )

    return (
        <ChatLayout
            title='Chat'
            breadcrumbItems={[
                {title: 'Chats', href: '/profile/chats'},
                {title: 'Chat'}
            ]}
            isParticularChat={true}
        >
            <div className="flex flex-col flex-1 gap-4 relative">
                <Card>
                    <div className="flex min-[450px]:flex-row flex-col items-end 
                                    min-[450px]:items-center justify-between gap-2">
                        <div className="flex gap-2 items-center">
                            <BasicLink 
                                to='/profile/chats'
                                icon={<ArrowLeftOutlined />}
                            />
                            <img 
                                src={chat.anotherParticipant?.avatar} 
                                alt="User Image" 
                                width='48'
                                className="rounded-full" 
                            />
                            <div className="">
                                <div className="text-2xl">{chat.anotherParticipant?.username}</div>
                                <div className="text-xl text-(--color-grey-500)">online</div>
                            </div>
                        </div>
                        <Popconfirm
                            title="Delete the listing"
                            description="Are you sure to delete this listing?"
                            icon={<QuestionCircleOutlined className="text-red-500!" />}
                            onConfirm={() => onDeleteChatButtonClick()}
                        >
                            <Button 
                                icon={<DeleteOutlined  className="text-xl!" />}
                            />
                        </Popconfirm>
                    </div>
                </Card>
                <div className="flex flex-col flex-1 min-h-40 max-h-120 pb-10
                                overflow-y-auto gap-10 shadow-[inset_0_-12px_25px_-10px_rgba(126,126,126,0.21)]"              
                >
                    {messagesByDates.map(({date, messages}) => (
                        <div className="flex flex-col gap-4" key={date}>
                            <div className="flex justify-center text-(--color-grey-500)">{date}</div>
                            <div className="flex flex-col gap-6">
                                {messages.map(({messages, uuid}) => (
                                    <div className="" key={uuid}>
                                        <ChatMessagesGroup 
                                            messages={messages}
                                            onDeleteChatMessageButtonClick={onDeleteChatMessageButtonClick}
                                        />
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
                <div className="">
                    <ChatTextarea onSendMessage={onSendMessageSubmit} />
                </div>
            </div>
        </ChatLayout>
    )
}