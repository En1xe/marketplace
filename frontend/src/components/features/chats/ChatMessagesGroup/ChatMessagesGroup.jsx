import ChatMessageCard from "@comps/features/chats/ChatMessageCard/ChatMessageCard";

import user_img from '@assets/icons/basic-user-avatar.png'


export default function ChatMessagesGroup({messages, onDeleteChatMessageButtonClick}) {
    const firstMessage = messages[0]

    return (
        <div 
            className="flex gap-2 items-start" 
        >
            <img   
                width={40}
                src={firstMessage.author.avatar || user_img}
                alt="User Avatar"
                className="rounded-full"
            />
            <div className="flex flex-col gap-3 flex-1">
                <div className="flex gap-2">
                    <div className="font-medium">{firstMessage.author.username}</div>
                    <div className="text-(--color-grey-500)">{firstMessage.createdAt}</div>
                </div>
                <div className="flex flex-col gap-4">
                    {messages.map(message => (
                        <div className="" key={message.uuid}>
                            <ChatMessageCard 
                                message={message}
                                onDeleteChatMessageButtonClick={onDeleteChatMessageButtonClick}
                                messageAuthorId={firstMessage.author.id}
                            />
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}