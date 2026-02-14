import { Popconfirm, Button } from "antd"
import { 
    CheckOutlined, 
    StopOutlined, 
    EditOutlined, 
    DeleteOutlined, 
    QuestionCircleOutlined 
} from "@ant-design/icons"

import BasicLink from "@comps/ui/Links/BasicLink/BasicLink"


export default function profileTableColumns(onDelete) {
    return [
        {
            title: 'Ads',
            dataIndex: 'ads',
            key: 'ads',
            render: (text, record) => (
                <div className="flex items-center h-15 w-50">
                    <BasicLink to={`/listings/${record.uuid}`}>
                        <img 
                            alt='Listing Image' 
                            src={record.media[0]?.url}
                            width='60'
                            height='60'
                            className="rounded-lg"
                        />
                        <div className="text-(--color-dark-900) text-xl truncate">{record.title}</div>
                    </BasicLink>
                </div>
            )
        },
        {
            title: 'Date',
            key: 'date',
            sorter: (a, b) =>  new Date(a.created_at) - new Date(b.created_at),
            render: (text, record) => (
                <div className="text-(--color-grey-500)">
                    {record.createdAt}
                </div>
            )
        },
        {
            title: 'Prices',
            key: 'prices',
            sorter: (a, b) => {
                if (a.is_price_negotiable && b.is_price_negotiable) return 0

                if (a.is_price_negotiable) return 1

                if (b.is_price_negotiable) return -1

                return a.price - b.price
            },
            render: (text, record) => (
                <div className="text-(--color-dark-700)">
                    {record.is_price_negotiable
                        ? 'Price negotiable'
                        : `\$${record.price}`
                    }
                </div>
            )
        },
        {
            title: 'Status',
            dataIndex: 'status',
            key: 'status',
            sorter: (a, b) => {
                if (a.is_active === b.is_active) {
                    return 0
                }

                return a.is_active ? -1 : 1
            },
            defaultSortOrder: 'ascend',
            render: (text, record) => (
                <div className="">
                    {
                        record.is_active
                        ? <div className="text-(--color-green-500) flex gap-2">
                            <CheckOutlined className="text-(--color-green-500)!" />
                            Active
                        </div>
                        : <div className="text-(--color-accent) flex gap-2">
                            <StopOutlined className="text-(--color-accent)!" />
                            Completed
                        </div>
                    }
                </div>
            )
        },
        {
            title: 'Action',
            dataIndex: 'action',
            key: 'action',
            render: (text, record) => (
                <div className="flex gap-3 max-[1200px]:flex-col">
                    <BasicLink 
                        to={`/profile/edit_listing/${record.uuid}`}
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
                        onConfirm={() => onDelete(record.uuid)}
                    >
                        <Button 
                            danger
                            icon={<DeleteOutlined />}
                        >
                            Delete
                        </Button>
                    </Popconfirm>
                </div>
            )
        },
    ] 
}