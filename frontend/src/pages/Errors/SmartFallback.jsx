import { getErrorType } from "@utils"

import ErrorPage from "./ErrorPage"


export default function SmartFallback({error}) {
    const errorType = getErrorType(error)

    switch (errorType) {
        case 'AUTH':
            return  <ErrorPage 
                        statusCode={error.status}
                    />
        case 'INVALID_DATA':
            return  <ErrorPage 
                        statusCode={error.status} 
                    />
        case 'NO_OBJECT_WAS_FOUND':
            return  <ErrorPage 
                        statusCode={error.status} 
                    />
        default:
            return <ErrorPage error='error' />
    }

}