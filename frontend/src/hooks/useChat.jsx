import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { message } from "antd";

import { getFormattedChat } from "@utils";

import { chatsService } from "@services/api/chats.service";
import { chatMessagesService } from "@services/api/chatMessages.service";

import useWebsocket from "./useWebsocket";


export default function useChat(userData, chatUuid) {
    const navigate = useNavigate()
    const {messages, sendMessage} = useWebsocket(chatUuid)

    const [chat, setChat] = useState({})

    useEffect(() => {
        if (messages.length < 1) return 

        const newMessage = messages.pop()
        handleAddChatMessage(newMessage)
    }, [messages])

    useEffect(() => {
        if (!userData || !chatUuid) return 

        const fetchChat = async () => {
            try {
                const chat = await chatsService.getChat(chatUuid)

                if (chat) {
                    const formattedChat = getFormattedChat(chat, userData)
                    setChat(formattedChat)
                }
            } catch (error) {
                message.error('No chat was received')
            }
        }

        fetchChat()
    }, [userData, chatUuid])

    const handleAddChatMessage = (chatMessage) => {
        setChat(prev => ({
            ...prev,
            messages: [...prev.messages, chatMessage]
        }))
    }

    const handleUpdateChatMessage = (chatMessage) => {
        const filteredMessages = chat.messages.filter(message => message.uuid !== chatMessage.uuid)
        filteredMessages.push(chatMessage)

        setChat(prev => ({
            ...prev,
            messages: [...filteredMessages]
        }))
    }

    const handleDeleteChatMessage = (chatUuid) => {
        const filteredMessages = chat.messages.filter(message => message.uuid !== chatUuid)

        setChat(prev => ({
            ...prev,
            messages: [...filteredMessages]
        }))
    }

    const onDeleteChatButtonClick = async () => {
        try {
            const response = await chatsService.deleteChat(chatUuid)

            navigate('/profile/chats', {replace: true})
        } catch (error) {
            message.error('The chat was not deleted')
        }
    }

    const onDeleteChatMessageButtonClick = async (chatMessageUuid) => {
        try {
            const response = await chatMessagesService.deleteChatMessage(chatMessageUuid)

            handleDeleteChatMessage(chatMessageUuid)
            message.success('Chat message was deleted successfully')
        } catch (error) {
            message.error('The chat message was not deleted')
        }
    }

    return {
        chat, 
        sendMessage,
        handleAddChatMessage,
        handleUpdateChatMessage,
        handleDeleteChatMessage,
        onDeleteChatButtonClick,
        onDeleteChatMessageButtonClick,
    }
}