import { useState, useEffect } from 'react';


export default function useUserFormFields(userData) {
    const [formFields, setFormFields] = useState([])
    
    useEffect(() => {
        if (!userData) return

        const fields = [
            {
                name: 'file',
                type: 'image',
                label: 'User Image',
                initialValue: userData.avatar,
                required: true, 
            },
            {
                name: 'username',
                type: "text",
                placeholder: 'Username',
                label: 'Username',
                required: true,
                initialValue: userData.username
            }
        ]

        setFormFields(fields)
    }, [userData])

    return {formFields}
}