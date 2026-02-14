import { Badge } from 'antd'
import { CommentOutlined  } from '@ant-design/icons'

import BasicLink from '../BasicLink/BasicLink'


export default function ChatLink({text='', showDot=false, className='', ...props}) {
    return (
        <BasicLink 
            to='/profile/chats'
            className={className}
            size='large'
            type='link' 
            icon={
                <Badge dot={showDot}>
                    <CommentOutlined
                        className='text-4xl! text-(--color-grey-500)! 
                        hover:text-(--color-grey-500-hover)! flex! items-center!' 
                    />
                </Badge>
            } 
            {...props}
        >
            {text}
        </BasicLink>
    )
}