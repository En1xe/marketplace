import { useState, useEffect } from "react"


export const useAsyncThrow = () => {
    const [error, setError] = useState()

    useEffect(() => {
        if (error) {
            throw error
        }
    }, [error])

    return {setError}
}