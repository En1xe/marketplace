export const getFormattedDate = (date) => {
    const options = {
        month: 'short',
        day: 'numeric',
    }

    if (date.getFullYear() !== new Date().getFullYear()) {
        options.year = 'numeric'
    }

    return new Intl.DateTimeFormat('en-EN', options).format(date)
} 


export const getFormattedTime = (date) => {
    return new Intl.DateTimeFormat('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    }).format(date)
}


export const getFormattedDataFromString = (string) => {
    if (!string) return ''

    const date = new Date(string)
    return getFormattedDate(date)
}
