import { Upload, message } from 'antd'
import BasicButton from '../../Buttons/BasicButton/BasicButton'


export default function UserImageUpload({fieldName, setAvatar}) {
    return (
        <Upload
            maxCount={1}
            beforeUpload={file => {
                const isImage = file.type.includes('image')

                if (!isImage) {
                    message.error(`${file.name} is not an image file`)
                    return isImage || Upload.LIST_IGNORE;
                }
                
                setAvatar(fieldName, file)
                return false
            }}
        >
            <BasicButton 
                type='primary'
                className='p-4!'
            >
                Choose Image
            </BasicButton>
        </Upload>
    )
}