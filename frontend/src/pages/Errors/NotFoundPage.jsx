import { ArrowLeftOutlined } from "@ant-design/icons"

import AppLayout from "@comps/layout/Layouts/BasicLayout/Layout"

import BasicButton from "@comps/ui/Buttons/BasicButton/BasicButton"


export default function NotFoundPage() {
    return (
        <AppLayout
            title='Error'
            breadcrumbItems={[
                {title: 'Home'},
                {title: '404 Error Page'},
            ]}
        >
            <div className="flex items-center gap-8 flex-col">
                <div className="text-7xl text-(--color-accent)">
                    Status: 404
                </div>
                <div className="flex flex-col items-center gap-4">
                    <div className="text-(--color-grey-500)">
                        Page was not found
                    </div>
                    <BasicButton 
                        size='large'
                        type='primary'
                        className='py-4! px-2!'
                        icon={<ArrowLeftOutlined />}
                        onClick={() => window.location.href = '/'}
                    >
                        Go Back Home
                    </BasicButton>
                </div>
            </div>
        </AppLayout>
    )
}