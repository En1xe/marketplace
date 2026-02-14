import { httpService } from "./base.service";


class RedirectTokensService {
    async createRedirectToken(code) {
        try {
            const response = await httpService.post('/redirect_tokens', code)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async getRedirectTokenData(token) {
        try {
            const response = await httpService.get(`/redirect_tokens?token=${token}`)
            return response.data
        } catch (error) {
            throw error
        }
    }
}

export const redirectTokenService = new RedirectTokensService()