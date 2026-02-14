import { Typography } from 'antd'

import AppLayout from "../BasicLayout/Layout"

import {AUTH_PAGE_INFO_DATA} from './AuthLayout.constants.jsx'


export default function AuthLayout({children, breadcrumbItems}) {
    return (
        <AppLayout
            breadcrumbItems={breadcrumbItems}
        >
            <div className="grid lg:grid-cols-2 gap-25 justify-center items-center">
                <ul className="flex-col gap-25 hidden lg:flex">
                    {AUTH_PAGE_INFO_DATA.map(({title, description, img}) => (
                        <li className="flex gap-8" key={title}>
                            {img}
                                <div className="flex flex-col gap-4">
                                <Typography.Title level={4} className='m-0!'>
                                    {title}
                                </Typography.Title>
                                <div className="text-(--color-grey-500)">
                                    {description}
                                </div>
                            </div>
                        </li>
                    ))}
                </ul>
                <div className="">
                    {children}
                </div>
            </div>
        </AppLayout>
    )
}