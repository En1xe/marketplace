import { Button } from "antd"
import { 
    EditOutlined
} from "@ant-design/icons"


export default function EditButton({onClick}) {
    return (
        <Button 
            type='default'
            className='px-3!'
            onClick={onClick}
            icon={<EditOutlined />} 
        >
            Edit
        </Button>
    )
}