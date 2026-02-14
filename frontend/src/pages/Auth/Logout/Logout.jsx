import { useEffect } from "react"

import useAuth from "@hooks/useAuth"


export default function LogoutPage() {
    const { logout } = useAuth()

    useEffect(() => {
        logout()
    }, [])
    
    return (
        <>
        </>
    )
}