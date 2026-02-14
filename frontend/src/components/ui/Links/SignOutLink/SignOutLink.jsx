import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { Modal, Button } from 'antd'
import { LogoutOutlined } from '@ant-design/icons'

import BasicButton from '@comps/ui/Buttons/BasicButton/BasicButton';


export default function SignOutLink({onConfirm}) {
    const navigate = useNavigate()
    const [modalOpen, setModalOpen] = useState(false);

    const onModalConfirm = () => {
        navigate('/auth/signout')
    }

    return (
        <>
            <BasicButton 
                type='link' 
                className='p-0! text-(--color-black-900)!'
                icon={<LogoutOutlined className='text-xl!' />}
                onClick={() => setModalOpen(true)}
            >
                Log Out
            </BasicButton>
            <Modal
                title="Log Out"
                centered
                open={modalOpen}
                onOk={() => onModalConfirm()}
                onCancel={() => setModalOpen(false)}
            >
                <div className="">
                    Are you sure you want to log out of your account?
                </div>
            </Modal>
        </>
    )
}