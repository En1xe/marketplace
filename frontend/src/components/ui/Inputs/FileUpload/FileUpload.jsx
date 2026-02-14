import { Upload } from "antd"
import { PlusOutlined } from '@ant-design/icons'


export default function FileUpload({formDataName, fileList = [], setFileList, maxFiles = 8}) {
    const handleChange = (info) => {
        setFileList(formDataName, info.fileList)
    }

    return (
        <Upload
            listType="picture-card"
            fileList={fileList}
            onChange={handleChange}
            beforeUpload={() => false}
        >
            {fileList.length >= maxFiles ? null : (
                <button style={{ border: 0, background: 'none' }} type="button">
                    <PlusOutlined />
                    <div style={{ marginTop: 8 }}>Upload</div>
                </button>   
            )}
        </Upload>
    )
}