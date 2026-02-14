import { Empty } from "antd";

import ChatLayout from "@comps/layout/Layouts/ChatLayout/ChatLayout";


export default function ChatsPage() {
    return (
        <ChatLayout
            title='Chats'
            breadcrumbItems={[
                {title: 'Chats'}
            ]}
        >
            <div className="w-full flex justify-center items-center">
                <Empty />
            </div>
        </ChatLayout>
    )
}