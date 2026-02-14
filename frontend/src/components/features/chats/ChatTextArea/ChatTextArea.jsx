import { Input } from 'antd'

import BasicButton from '@comps/ui/Buttons/BasicButton/BasicButton'

import { SendOutlined } from '@ant-design/icons'
import { useEffect, useRef, useState } from 'react'


export default function ChatTextarea({ onSendMessage }) {
    const textAreaRef = useRef(null)
    const [localText, setLocalText] = useState('')

    const handleLocalTextChange = (e) => {
        setLocalText(e.target.value)
    }

    const handleChatMessageButtonClick = () => {
        onSendMessage(localText)
        setLocalText('')
    }

    const handleKeyDown = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            if (localText.trim()) {
                onSendMessage(localText)
                setLocalText('')
            }
        }
    }

    return (
        <div className="flex gap-2 items-end">
            <Input.TextArea
                ref={textAreaRef} 
                rows={1}
                className='resize-none! py-3!'
                value={localText}
                onChange={handleLocalTextChange}
                onKeyDown={handleKeyDown}
                placeholder='Type your message...'
                autoSize={{minRows: 1, maxRows: 5}}
            />
            <BasicButton
                disabled={!localText.trim()}
                onClick={handleChatMessageButtonClick}
                htmlType="submit"
                size='large'
                type='primary'
                icon={<SendOutlined />}
            />
        </div>
    )
}