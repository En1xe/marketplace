import { message } from 'antd'

import { useNavigate } from 'react-router-dom'

import { MessageOutlined } from '@ant-design/icons'

import BasicButton from '@comps/ui/Buttons/BasicButton/BasicButton'

import useAuth from '@hooks/useAuth'

import { chatsService } from '@services/api/chats.service'


export default function SendMessageButton({listing}) {
    const navigate = useNavigate()
    const { userData } = useAuth()

    const onSendMessageButtonClick = async () => {
        let chat = null

        if (!userData || Object.keys(userData).length === 0) {
            navigate('/auth/signin')
        }

        try {
            const formData = new FormData()
            formData.append('listing_id', listing.id)

            chat = await chatsService.createChatWithParticipants(formData)
        } catch (error) {
            message.error('Chat was not created')
            console.log(error)
        }

        try {
            if (!chat) {
                const chats = await chatsService.getChats({listing_id: listing.id})
                
                if (chats?.length > 0) {
                    chat = chats[0]
                }
            }
        } catch (error) {
            console.log(error)
        }

        if (chat) {
            navigate(`/profile/chats/${chat.uuid}`)
        }
    }

    return (
        <BasicButton
            className='bg-(--color-accent)! hover:bg-(--color-accent-hover)! 
            w-full! py-6! font-medium!'
            type='primary'
            icon={<MessageOutlined className='text-xl!' />}
            onClick={() => onSendMessageButtonClick()}
        >
            Send Message
        </BasicButton>
    )
}