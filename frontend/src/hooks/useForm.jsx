import { useState, useEffect } from "react";

export default function useFormData(fields) {
    const [error, setError] = useState('')
    const [formData, setFormData] = useState(() => {
        return fields.reduce((acc, item) => {
            acc[item.name] = item.initialValue
            return acc
        }, {})
    })

    useEffect(() => {
        const setFormDataByFields = () => {
            const result = fields.reduce((acc, item) => {
                acc[item.name] = item.initialValue
                return acc
            }, {})

            setFormData(result)
        }

        setFormDataByFields()
    }, [fields])

    const setInputOTPChange = (name, value) => {
        setFormData(
            prevState => ({
                ...prevState,
                [name]: value
            })
        )
    }

    const setInputChange = (e) => {
        const { name, value } = e.target

        setFormData(
            prevState => ({
                ...prevState,
                [name]: value
            })
        )
    }

    const setCheckBoxChange = (name, event) => {
        const checked = event.target.checked
        
        setFormData(
            prevState => ({
                ...prevState,
                [name]: checked
            })
        )
    }

    const setUploadFilesChange = (name, fileList) => {
        setFormData(
            prevState => ({
                ...prevState,
                [name]: fileList
            })
        )
    }

    const getPreparedFormDataForUpload = () => {
        const filesUploadFormData = new FormData()
        const preparedFormData = new FormData()
        const existingFilesUploadArr = []

        Object.keys(formData).forEach(key => {
            const value = formData[key]

            if (key === 'files') {
                value.forEach((file) => {
                    if (file.originFileObj) {
                        filesUploadFormData.append('files', file.originFileObj)
                    } else if (file.url) {
                        existingFilesUploadArr.push(file.url)
                    }
                })
            } else {
                preparedFormData.append(key, value)
            }
        })

        filesUploadFormData.append('existing_files', existingFilesUploadArr)

        return [preparedFormData, filesUploadFormData]
    }

    return {
        formData, 
        setInputChange, 
        setCheckBoxChange, 
        setInputOTPChange, 
        setUploadFilesChange,
        getPreparedFormDataForUpload,
        error, 
        setError
    }
}