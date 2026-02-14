import { Typography, Breadcrumb } from 'antd'


export default function CustomBreadcrumb({title, breadcrumbItems}) {
    return (
        <div 
            className="flex justify-center items-center py-5 md:py-13  
                flex-col bg-[url('@assets/images/breadcrumb-image.jpg')] 
                bg-no-repeat bg-cover relative before:absolute 
                before:bg-[#191F33]/50 before:inset-0 before:backdrop-blur-[2px]"  
            style={{backgroundPositionY: '18%'}}
        >
            <Typography.Title className='relative text-white!'>
                {title || 'Ad List'}
            </Typography.Title>
            <Breadcrumb
                className='relative' 
                items={breadcrumbItems}
            />
        </div>
    )
}