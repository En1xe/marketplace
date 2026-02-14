import { httpService } from "./base.service";

class AuthService {
    async login(credentials) {
        try {
            const response = await httpService.post('/auth/login', credentials)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async register(userData) {
        try {
            const response = await httpService.post('/users', userData)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async logout() {
        try {
            const response = await httpService.post('/auth/logout')
            return response.data
        } catch (error) {
            throw error
        }
    }

    async verify_token(credentials) {
        try {
            const response = await httpService.post('/auth/tokens/verify', credentials)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async set_new_password(userUuid, data) {
        try {
            const response = await httpService.patch(`/users/${userUuid}`, data)
            return response.data
        } catch (error) {
            throw error
        }
    }
}

export const authService = new AuthService()