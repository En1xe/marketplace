import { MailOutlined } from '@ant-design/icons'

import BasicButton from '@comps/ui/Buttons/BasicButton/BasicButton'


export default function SendEmailButton() {
    return (
        <BasicButton
            className='bg-(--color-grey-50)! hover:bg-(--color-grey-50-hover)! 
            w-full! py-6! text-black! font-medium!'
            type='primary'
            icon={<MailOutlined className='text-xl!' />}
        >
            Message via email
        </BasicButton>
    )
}