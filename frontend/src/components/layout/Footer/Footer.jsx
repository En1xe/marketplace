import { Layout, Typography, Divider, Button } from 'antd'
import {ArrowUpOutlined} from '@ant-design/icons'

import BasicLink from '@comps/ui/Links/BasicLink/BasicLink'

import {scrollToTop} from '@utils'

import { FOOTER_DATA } from './Footer.constants'


export default function Footer() {
    return (
        <Layout.Footer 
            className='p-0!'
        >
            <div 
                className="container flex flex-col md:flex-row gap-6 justify-between 
                bg-(--color-dark-900) text-(--color-grey-500) py-12.5 lg:py-25"
            >
                {FOOTER_DATA.map(({title, are_links, data}) => (
                    <div 
                        className="flex flex-col md:gap-3 max-w-60" 
                        key={title}
                    >
                        <Typography.Title level={4} className='text-white!'>
                            {title}
                        </Typography.Title>
                        
                        <ul className="flex flex-col md:gap-2">
                            {data.map(text => (
                                <li className="" key={text}>
                                    {are_links 
                                        ? <BasicLink
                                            className='border-b-2! rounded-none! text-(--color-grey-500)! 
                                            hover:text-white! hover:border-b-solid! hover:border-b-(--color-accent)!
                                            active:border-b-(--color-accent)! active:text-white!' 
                                          >
                                            {text}
                                          </BasicLink>
                                        : text
                                    }
                                </li>
                            ))}
                        </ul>
                    </div>
                ))}
            </div>
            <div 
                className="container relative flex justify-between flex-col md:flex-row
                bg-(--color-dark-800) text-(--color-grey-500) py-10 md:py-6 "
            >
                <div className="">
                    Adfinity - Classified Listing © 2021. Design by&nbsp;
                    <span className='text-white'>Templatecookie</span>
                </div>
                <div className="flex items-center">
                    <div className="">
                        <BasicLink className='text-(--color-grey-500)! hover:text-white! active:text-white!'>
                            Privacy Policy
                        </BasicLink>
                    </div>
                    <Divider vertical className='bg-(--color-grey-500)!' />
                    <div className="">
                        <BasicLink className='text-(--color-grey-500)! hover:text-white! active:text-white!'>
                           Terms & Condition
                        </BasicLink>
                    </div>
                </div>
                <Button
                    className="absolute! w-14! h-14! flex! justify-center! items-center! text-white!
                    bg-(--color-dark-800)! rounded-full! right-25! -top-7! md:bottom-14!
                    border-(--color-dark-900)! border-5! before:content-none!
                    hover:bg-(--color-dark-800-hover)!"
                    onClick={() => scrollToTop('top-page-section')}
                >
                    <ArrowUpOutlined className='text-xl' />
                </Button>
            </div>
        </Layout.Footer>
    )
}