import { Link } from "react-router-dom"
import { Card, Typography, Skeleton, Space } from "antd"


export default function ListingCard({data, isLoading}) {
    const {title, media, price, is_price_negotiable, uuid, is_active} = data || {}
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
            <div className="flex flex-col gap-2">
                <div className="text-(--color-grey-500)">category</div>
                <Link to={`/listings/${uuid}`}>
                    <Typography.Title 
                        level={5} 
                        className='truncate! hover:text-(--color-accent)!'
                    >
                        {title}
                    </Typography.Title>
                </Link>
            </div>
            <div className="flex justify-between items-center">
                <div className="text-(--color-grey-500)">location</div>
                <div 
                    className={`font-medium text-xl 
                    ${is_active ? 'text-(--color-accent)' : 'text-(--color-grey-500)'}`}
                >
                    {is_price_negotiable 
                        ? 'Price negotiable'
                        : `${price} $`
                    }
                </div>
            </div>
        </Card>
    )
}