export const getErrorType = (error) => {
    if (error.status === 422) {
        return 'INVALID_DATA'
    } else if (error.status === 404) {
        return 'NO_OBJECT_WAS_FOUND'
    }  

    return error
}