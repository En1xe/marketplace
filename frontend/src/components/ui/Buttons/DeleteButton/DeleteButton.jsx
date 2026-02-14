import { Popconfirm, Button } from "antd"
import { 
    DeleteOutlined, 
    QuestionCircleOutlined 
} from "@ant-design/icons"


export default function DeleteButton({onConfirm}) {
    return (
        <Popconfirm
            title="Delete the listing"
            description="Are you sure to delete this listing?"
            icon={<QuestionCircleOutlined className="text-red-500!" />}
            onConfirm={onConfirm}
        >
            <Button 
                danger
                icon={<DeleteOutlined />}
            >
                Delete
            </Button>
        </Popconfirm>
    )
}