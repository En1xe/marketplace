import { httpService } from "./base.service";


class ChatMessagesService {
    async getChatMessages(...filters) {
        try {
            const params = new URLSearchParams()

            if (filters.length > 0) {
                for (const [key, value] of Object.entries(...filters)) {
                    params.append(key, value)
                }   
            }
            
            const queryString = params.toString()

            const response = await httpService.get(`/chats/messages?${queryString}`)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async getChatMessage(uuid) {
        try {
            const response = await httpService.get(`/chats/messages/${uuid}`)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async createChatMessage(data) {
        try {
            const response = await httpService.post('/chats/messages/', data)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async updateChatMessage(uuid, data) {
        try {
            const response = await httpService.patch(`/chats/messages/${uuid}`, data)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async deleteChatMessage(uuid) {
        try {
            const response = await httpService.delete(`/chats/messages/${uuid}`)
            return response.data
        } catch (error) {
            throw error
        }
    }
}

export const chatMessagesService = new ChatMessagesService()