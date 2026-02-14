import { createContext, useEffect, useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";

import { authService } from "@services/api/auth.service"
import { usersService } from "@services/api/users.service"
import { verificationCodesService } from "@services/api/verificationCodes.service"


export const AuthContext = createContext()

export default function AuthProvider({children}) {
    const navigate = useNavigate()
    const [isLoading, setIsLoading] = useState(true)
    const [userData, setUserData] = useState(null)

    useEffect(() => {
        const fetchUserData = async () => {
            const token = localStorage.getItem('access')
            
            if (!token) {
                setIsLoading(false)
                return
            }

            const userData = await getUserByToken()
            setUserData(userData)
            setIsLoading(false)
        }

        fetchUserData()
    }, [])

    const getUserByToken = useCallback(async (credentials) => {
        try {
            const data = await usersService.getUserByToken(credentials)
            return data
        } catch (error) {
            setIsLoading(false)
            console.log(error)
        }
    }, [])

    const login = async (credentials) => {
        try {
            const data = await authService.login(credentials)

            const token = data?.access_token
            if (!token) {
                throw new Error('no token')
            }

            localStorage.setItem('access', token)

            const userData = await getUserByToken()
            setUserData(userData)

            return userData
        } catch (error) {
            throw error
        }
    }

    const logout = async () => {
        try {
            const response = await authService.logout()

            if (response?.success) {
                localStorage.removeItem('access')
                setUserData(null)
                navigate('/auth/signin', {replace: true})
            }
        } catch (error) {
            console.log(error)
        }
    }

    const register = async (userData) => {
        try {
            const data = await authService.register(userData)

            return data
        } catch (error) {
            throw error
        }
    }

    const getUserByEmail = async (email) => {
        try {
            const data = await usersService.get_user_by_email({email: email})

            return data
        } catch (error) {
            throw error
        }
    }

    const getUserByUUID = async (uuid, detail=false) => {
        try {
            const data = await usersService.getUserByUUID(uuid, detail)

            return data
        } catch (error) {
            throw error
        }
    }

    const getVerificationCode = async (verificationCodeUuid) => {
        try {
            const data = await verificationCodesService.getVerificationCode(verificationCodeUuid)

            return data
        } catch (error) {
            throw error
        }
    }

    const createVerificationCode = async (verificationCodeData) => {
        try {
            const data = await verificationCodesService.createVerificationCode(verificationCodeData)

            return data
        } catch (error) {
            throw error
        }
    }

    const validateVerificationCode = async (uuid) => {
        try {
            const data = await verificationCodesService.validateVerificationCode(uuid)

            return data
        } catch (error) {
            throw error
        }
    }

    const confirmVerificationCode = async (uuid, verificationCode) => {
        try {
            const data = await verificationCodesService.confirmVerificationCode(uuid, verificationCode)

            return data
        } catch (error) {
            throw error
        }
    }

    const setNewPassword = async (userUuid, password) => {
        try {
            const data = await authService.set_new_password(userUuid, password)

            return data
        } catch (error) {
            throw error
        }
    }

    const updateUserWithinRecovery = async (updateUserWithinRecoveryData) => {
        try {
            const data = await usersService.updateUserWithinRecovery(updateUserWithinRecoveryData)

            return data
        } catch (error) {
            throw error
        }
    }

    const value = { 
        userData,
        isLoading,
        login, 
        register, 
        logout,
        getUserByEmail, 
        getUserByUUID,
        createVerificationCode,
        validateVerificationCode,
        confirmVerificationCode,
        setNewPassword,
        getVerificationCode,
        getUserByToken,
        updateUserWithinRecovery
    }

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    )
}