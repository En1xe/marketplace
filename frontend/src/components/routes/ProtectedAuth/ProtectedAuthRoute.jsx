import { useLocation, Navigate } from "react-router-dom";

import useAuth from "@hooks/useAuth";


export default function ProtectedAuthRoute({children}) {
    const location = useLocation()

    const { userData, isLoading } = useAuth()

    if (isLoading) {
        return null
    }

    if (!userData || Object.keys(userData).length === 0) {
        return <Navigate to='/auth/signin' state={{from: location}} />
    }
    

    return children
}