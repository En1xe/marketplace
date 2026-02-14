import { Button } from "antd"

import { combineClasses } from "@utils"


export default function BasicButton({className, children, ...props}) {
    return (
        <Button
            className={combineClasses(
                'p-0!', 
                className
            )}
            {...props}
        >
            {children}
        </Button>
    )
}