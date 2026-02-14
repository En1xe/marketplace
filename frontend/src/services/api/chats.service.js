import { httpService } from "./base.service";


class ChatsService {
    async getChats(...filters) {
        try {
            const params = new URLSearchParams()

            if (filters.length > 0) {
                for (const [key, value] of Object.entries(...filters)) {
                    params.append(key, value)
                }   
            }
            
            const queryString = params.toString()

            const response = await httpService.get(`/chats?${queryString}`)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async getChat(uuid) {
        try {
            const response = await httpService.get(`/chats/${uuid}`)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async createChat(data) {
        try {
            const response = await httpService.post('/chats', data)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async createChatWithParticipants(data) {
        try {
            const response = await httpService.post('/chats/with_participants', data)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async updateChat(uuid, data) {
        try {
            const response = await httpService.patch(`/chats/${uuid}`, data)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async deleteChat(uuid) {
        try {
            const response = await httpService.delete(`/chats/${uuid}`)
            return response.data
        } catch (error) {
            throw error
        }
    }
}

export const chatsService = new ChatsService()