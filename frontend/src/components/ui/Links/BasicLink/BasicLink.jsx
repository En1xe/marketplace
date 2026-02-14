import { Button } from "antd"
import { Link } from 'react-router-dom';

import { combineClasses } from "@utils"


export default function BasicLink({className, to, children, ...props}) {
    return (
        <Link to={to} className="inline-block h-max">
            <Button
                type='link'
                className={combineClasses(
                    'p-0! flex!', 
                    className
                )}
                {...props}
            >
                {children}
            </Button>
        </Link>
    )
}