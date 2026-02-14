import { formatDistanceToNow } from 'date-fns'
import { enUS } from 'date-fns/locale'

import { getFormattedDate, getFormattedTime } from "./dates"
import { message } from 'antd'


export const getLastMessageTime = (createdAt) => {
    if (!createdAt) return ''

    const date = new Date(createdAt)
    
    return formatDistanceToNow(date, {
        addSuffix: true,
        locale: enUS
    })
}


const getAnotherParticipant = (chat, userId) => {
    const anotherChatParticipantArr = chat.participants.filter(({participant_id}) => {
        return participant_id !== userId
    })

    return anotherChatParticipantArr 
            ? anotherChatParticipantArr[0].participant
            : {}
}


export const getFormattedChats = (chats, userId) => {
    let formattedChats = []

    chats.forEach((chat) => {
        const anotherChatParticipant = getAnotherParticipant(chat, userId)

        const formattedChat = {
            uuid: chat.uuid,
            anotherParticipant: anotherChatParticipant,
            lastMessage: chat.last_message,
            listing: chat.listing
        }

        formattedChats.push(formattedChat)
    })

    return formattedChats
}


export const getFormattedChat = (chat, currentUser) => {
    const anotherChatParticipant = getAnotherParticipant(chat, currentUser.id)

    return {
        id: chat.id,
        uuid: chat.uuid,
        messages: chat.messages,
        currentParticipant: currentUser,
        anotherParticipant: anotherChatParticipant,
        listing: chat.listing
    }
}

export const getFormattedChatMessages = (messages, currentUser, anotherUser) => {
    if (!messages) return []

    const messagesByDates = []

    messages.forEach(({id, uuid, chat_id, text, author_id, created_at}) => {
        const date = new Date(created_at)
        const formattedDate = getFormattedDate(date)

        const messagesByCurrentDate = messagesByDates.find(item => item.date === formattedDate)

        const formattedMessage = {
            id,
            uuid,
            text,
            chatId: chat_id,
            createdAt: getFormattedTime(date),
            createdAtDate: created_at,
            author: author_id === currentUser.id ? currentUser : anotherUser
        }

        if (messagesByCurrentDate) {
            messagesByCurrentDate.messages.push(formattedMessage)
        } else {
            messagesByDates.push({
                date: formattedDate,
                messages: [formattedMessage]
            })
        }
    })

    messagesByDates.sort((a, b) => {
        const firstDate = new Date(a.date)
        const secondDate = new Date(b.date)

        return firstDate - secondDate
    })

    messagesByDates.forEach(({date, messages}) => {
        const formattedMessages = []
        
        const sortedMessages = [...messages]
        sortedMessages.sort((a, b) => {
            const firstDate = new Date(a.createdAtDate)
            const secondDate = new Date(b.createdAtDate)

            return secondDate - firstDate
        })

        sortedMessages.forEach(message => {

            if (formattedMessages.length > 0) {

                const lastMessage = formattedMessages.at(-1).messages.at(-1)

                if (
                    lastMessage.createdAt === message.createdAt && 
                    lastMessage.author.id === message.author.id
                ) {
                    formattedMessages.at(-1).messages.push(message)
                    return
                }
            } 

            formattedMessages.push({
                uuid: crypto.randomUUID(),
                messages: [message]
            })
        })

        const currentMessagesByDates = messagesByDates.filter(obj => obj.date === date)[0]
        formattedMessages.reverse()
        currentMessagesByDates.messages = formattedMessages
    })

    return messagesByDates
}