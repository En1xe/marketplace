import BasicButton from '@comps/ui/Buttons/BasicButton/BasicButton'

import RenderFormField from '../RenderFormField'
import { combineClasses } from '@utils'


export default function BasicForm({
    error, 
    onSubmit, 
    fields, 
    formData, 
    setInputChange, 
    setInputOTPChange,
    setCheckBoxChange,
    submitButtonText, 
    submitButtonClassName,
    setUploadFilesChange,
    extraActions,
}) {
    return (
        <form 
            onSubmit={onSubmit}
            className="flex flex-col gap-8"
        >
            <ul className='flex flex-col gap-4'>
                {fields.map((field) => (
                    <div key={field.name} className='flex'>
                        <li className={`flex gap-2 flex-1 flex-col`}>
                            {field.label && field.type !== 'checkbox' && 
                                <label htmlFor={field.name}>
                                    {field.label}
                                </label>
                            }
                            {RenderFormField(
                                field, 
                                formData, 
                                setInputChange, 
                                setInputOTPChange,
                                setCheckBoxChange,
                                setUploadFilesChange
                            )}
                        </li> 
                    </div> 
                ))}
                <div className="">
                    {extraActions}
                </div>
            </ul>

            {error && 
                <div className='text-red-500'>
                    {error}
                </div>
            }
            
            <BasicButton 
                htmlType='submit'
                type='text' 
                size='large' 
                className={
                    combineClasses(
                        'w-full bg-(--color-accent)! \
                        text-white! hover:bg-(--color-accent-hover)! py-6!',
                        submitButtonClassName
                )}
            >
                {submitButtonText}
            </BasicButton>
        </form>
    )
}