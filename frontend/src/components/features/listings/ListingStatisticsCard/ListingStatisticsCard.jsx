import { Link } from "react-router-dom"
import { Card, Typography, Skeleton, Space, Popconfirm, Button } from "antd"
import { EditOutlined, DeleteOutlined, QuestionCircleOutlined } from "@ant-design/icons"

import BasicLink from "@comps/ui/Links/BasicLink/BasicLink"


export default function ListingStatisticsCard({data, isLoading}) {
    const {title, media, price, is_price_negotiable, uuid, is_active, createdAt} = data || {}
    const imgUrl = media ? media[0]?.url : ''

    if (isLoading) {
        return (
            <div className="flex flex-col gap-4">
                <Skeleton.Node active style={{ width: '100%', height: 200 }} />
                <Skeleton active paragraph={{ rows: 4 }} />
            </div>
        )
    }

    return (
        <Card
            cover={
                <div className={`relative ${is_active ? 'group' : ''}`}>
                    <Link to={`/listings/${uuid}`}>
                        <img 
                            alt='Listing Image' 
                            src={imgUrl} 
                            className={`bg-cover bg-center object-contain w-full h-50 
                                ${!is_active ? 'opacity-60' : ''}`}
                        />
                        <div className="absolute inset-0 opacity-0 bg-black/30 backdrop-blur-[2px] flex justify-center 
                        items-center group-hover:opacity-100 rounded-tl-xl rounded-tr-xl cursor-pointer duration-200">
                            <Space vertical align="center" className="text-white">
                                View Details 
                            </Space>
                        </div>
                    </Link>
                </div>
            }
        >
            <Link to={`/listings/${uuid}`}>
                <Typography.Title 
                    level={5} 
                    className='truncate! hover:text-(--color-accent)!'
                >
                    {title}
                </Typography.Title>
            </Link>
            <div className="flex flex-col gap-4">
                <div className="flex flex-col gap-1">
                    <div>
                        Price:&nbsp;
                        {is_price_negotiable 
                            ? 'Price negotiable'
                            : `${price} $`
                        }
                    </div>
                    <div className="">
                        Date: {createdAt}
                    </div>
                    <div className="">
                        Status:&nbsp;
                        {
                            is_active
                            ? <span className="text-(--color-green-500)">Active</span>
                            : <span className="text-(--color-accent)">Completed</span>
                        }
                    </div>
                </div>
                <div className="flex gap-3">
                    <BasicLink 
                        to={`/profile/edit_listing/${uuid}`}
                        type='default'
                        className='px-3!'
                        icon={<EditOutlined />} 
                    >
                        Edit
                    </BasicLink>
                    <Popconfirm
                        title="Delete the listing"
                        description="Are you sure to delete this listing?"
                        icon={<QuestionCircleOutlined className="text-red-500!" />}
                        onConfirm={() => onDelete(uuid)}
                    >
                        <Button 
                            danger
                            icon={<DeleteOutlined />}
                        >
                            Delete
                        </Button>
                    </Popconfirm>
                </div>
            </div>
        </Card>
    )
}