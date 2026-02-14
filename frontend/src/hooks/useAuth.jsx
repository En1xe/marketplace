import { AuthContext } from "@context/AuthContext";
import { useContext } from "react";


export default function useAuth() {
    const context = useContext(AuthContext)

    if (!context) {
        console.log('No auth context')
        return
    }

    return context
}