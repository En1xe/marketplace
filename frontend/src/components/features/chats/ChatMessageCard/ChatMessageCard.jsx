import { Dropdown } from "antd";
import { MoreOutlined } from "@ant-design/icons";

import DeleteButton from "@comps/ui/Buttons/DeleteButton/DeleteButton";

import useAuth from "@hooks/useAuth";


export default function ChatMessageCard({
    message, 
    onDeleteChatMessageButtonClick, 
    messageAuthorId
}) {
    const { userData } = useAuth()

    const dropDownItems = (chatMessageUuid) => {
        return [
            {
                key: '2',
                label: (
                    <DeleteButton 
                        onConfirm={() => onDeleteChatMessageButtonClick(chatMessageUuid)} 
                    />
                )
            }
        ]
    } 

    return (
        <div 
        className="flex justify-between"
        >
            <div className="">
                {message.text}
            </div>
            <div 
                className={messageAuthorId === userData.id ? 'block' : 'hidden'}
            >
                <Dropdown 
                    trigger={['click']} 
                    menu={{items: dropDownItems(message.uuid)}}
                >
                    <div className="">
                        <MoreOutlined className="text-xl!" />
                    </div>
                </Dropdown>
            </div>
        </div>
    )
}