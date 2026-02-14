import { Input } from 'antd'

import { combineClasses } from '@utils'


export default function BasicInput({className, ...props}) {
    return (
        <Input
            className={combineClasses('p-0! m-0!', className)}
            {...props}
        />
    )
}