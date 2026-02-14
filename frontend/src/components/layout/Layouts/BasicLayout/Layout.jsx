import { Layout } from 'antd'

import Header from '../../Header/Header'
import Footer from '../../Footer/Footer'
import CustomBreadcrumb from '../../Breadcrumb'


export default function AppLayout({title, children, breadcrumbItems}) {
    return (
        <Layout className='flex flex-col h-full xl:gap-12.5 lg:gap-10 gap-5'>
            <div className="" id='top-page-section'>
                <Header />
                <CustomBreadcrumb 
                    breadcrumbItems={breadcrumbItems}
                    title={title}
                />
            </div>
            <Layout.Content className=''>
                <div className="container">
                    {children}
                </div>
            </Layout.Content>
            <Footer />
        </Layout>
    )
}