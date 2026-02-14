import { HeartOutlined, HeartFilled } from "@ant-design/icons"

import BasicButton from "../BasicButton/BasicButton"


export default function FavoriteButton({isActive, onClick, isDisabled}) {
    return (
        <BasicButton 
            onClick={onClick}
            size='large'
            disabled={isDisabled}
            icon={isActive
                ? <HeartFilled className="text-red-400! text-2xl!" />
                : <HeartOutlined className="text-2xl!" />
            }
        />
    )
}