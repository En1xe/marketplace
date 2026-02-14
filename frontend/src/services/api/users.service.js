import { httpService } from "./base.service";


class UsersService {
    async getUserByToken(credentials) {
        try {
            const response = await httpService.get('/users/token', credentials)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async get_user_by_email(email) {
        try {
            const response = await httpService.post('/users/email', email)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async getUserByUUID(uuid, detail) {
        try {
            const config = {
                params: {
                    detail,
                }
            }
            const response = await httpService.get(`/users/${uuid}`, config)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async updateUserWithinRecovery(data) {
        try {
            const response = await httpService.patch('/users/redirect_token', data)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async updateUser(uuid, data) {
        try {
            const response = await httpService.patch(`/users/${uuid}`, data)
            return response.data
        } catch (error) {
            throw error
        }
    } 

    async uploadUserAvatar(uuid, data) {
        try {
            const response = await httpService.post(
                `/users/${uuid}/avatar`, 
                data,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                }
            )
            return response.data
        } catch (error) {
            throw error
        }
    } 
}

export const usersService = new UsersService()