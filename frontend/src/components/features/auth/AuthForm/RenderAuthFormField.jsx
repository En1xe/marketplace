import { Input } from 'antd'

import BasicInput from "@comps/ui/Inputs/BasicInput/BasicInput"


export default function RenderAuthFormField(field, formData, setInputChange, setInputOTPChange) {
    const {name, type, placeholder, required, ...props} = field

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
        default:
            return null
    }
}