import { Rate } from 'antd'

import user_img from '@assets/icons/basic-user-avatar.png'


export default function ReviewCard({data}) {
    const {name, rating, text, listing} = data

    return (
        <div className="flex gap-6">
            <img src={user_img} alt='User avatar' width={88} className='object-contain rounded-full' />
            <div className="flex flex-col gap-2.5">
                <div className="flex flex-col gap-1">
                    <div className="flex gap-1">
                        <Rate allowHalf defaultValue={rating} />
                        <div className="font-medium">{rating} Star Rating</div>
                    </div>
                    <div className="flex gap-2">
                        <div className="font-medium">{name}</div>
                        <div className="">
                            <span className='text-(--color-grey-500)'>Ads:</span>&nbsp;
                            <span className='text-(--color-dark-700)'>{listing}</span>
                        </div>
                    </div>
                </div>
                <div className="text-(--color-dark-700)">
                    {text}
                </div>
            </div>
        </div>
    )
}