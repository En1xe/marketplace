import { Input } from 'antd'
 
import { combineClasses } from "@utils"


export default function BasicTextarea({className, children, ...props}) {
    return (
        <Input.TextArea 
            className={combineClasses(
                'resize-none! h-30!', 
                className
            )}
            {...props}
        >
            {children}
        </Input.TextArea >
    )
}