import { Typography, Card } from 'antd'


export default function AuthBox({title, topChildren, bottomChildren, form}) {
    return (
        <Card className="">
            <div className="flex flex-col gap-8 p-4 lg:p-12.5">
                <div className="flex flex-col gap-6">
                    <div className="text-center">
                        <Typography.Title className='m-0!'>
                            {title}
                        </Typography.Title>
                    </div>
                </div>
                {topChildren}
                <div className="flex flex-col gap-4">
                    {form}
                </div>
                {bottomChildren}
            </div>
        </Card>
    )
}