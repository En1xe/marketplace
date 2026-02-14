import { Input, InputNumber, Checkbox, Rate, Upload } from 'antd'

import BasicTextarea from '@comps/ui/Textareas/BasicTextarea/BasicTextarea'
import BasicInput from "@comps/ui/Inputs/BasicInput/BasicInput"
import FileUpload from '@comps/ui/Inputs/FileUpload/FileUpload'
import UserImageUpload from '@comps/ui/Inputs/UserImageUpload/UserImageUpload'


export default function RenderFormField(
    field, 
    formData, 
    setInputChange, 
    setInputOTPChange, 
    setCheckBoxChange,
    setUploadFilesChange
) {
    const {
        name, 
        type, 
        placeholder, 
        required, 
        label, 
        defaultValue
    } = field

    switch (type) {
        case 'text':
        case 'email':
        case 'number':
            return (
                <BasicInput 
                    className='py-3! px-4!'
                    id={name}
                    name={name}
                    type={type}
                    value={formData[name]}
                    onChange={setInputChange}
                    placeholder={placeholder}
                    required={required || false}
                />
            )
        case 'rating':
            return (
                <Rate 
                    value={formData[name]}
                    onChange={(value) => setInputOTPChange(name, value)}
                    size='large' 
                />
            )
        case 'verifyCode':
            return (
                <Input.OTP 
                    name={name} 
                    value={formData[name]} 
                    onChange={(value) => setInputOTPChange(name, value)} 
                />
            )
        case 'password':
            return (
                <Input.Password 
                    className='py-3! px-4!'
                    id={name}
                    name={name}
                    placeholder={placeholder}
                    value={formData[name]}
                    onChange={setInputChange}
                    required={required || false}
                />
            )
        case 'price':
            return (
                <InputNumber
                    className='w-30!'
                    name={name} 
                    id={name}
                    value={formData[name]}
                    onChange={(value) => setInputOTPChange(name, value)}
                    min={0}
                    max={10000000}
                />
            )
        case 'checkbox':
            return (
                <Checkbox 
                    checked={formData[name]}
                    onChange={(e) => setCheckBoxChange(name, e)}
                    defaultValue={defaultValue}
                >
                    {label}
                </Checkbox>
            )
        case 'textarea':
            return (
                <BasicTextarea
                    name={name}
                    id={name}
                    value={formData[name]}
                    onChange={setInputChange}
                    placeholder={placeholder}
                    required={required}
                />
            )
        case 'files':
            return (
                <FileUpload 
                    formDataName={name}
                    fileList={formData[name]}
                    setFileList={setUploadFilesChange}
                />
            )
        case 'image':
            return (
                <div className="flex gap-3 items-center">
                    <img 
                        src={formData[name] || null}
                        alt="User Image"
                        className="rounded-full object-cover w-20 h-20 sm:w-25 sm:h-25"
                    />
                    <UserImageUpload 
                        fieldName={name}
                        setAvatar={setInputOTPChange}
                    />
                </div>
            )
        default:
            return null
    }
}