import { httpService } from "./base.service";

class VerificationCodesService {
    async getVerificationCode(verificationCodeUuid) {
        try {
            const response = await httpService.get(`/verification_codes/${verificationCodeUuid}`)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async createVerificationCode(data) {
        try {
            const response = await httpService.post('/verification_codes', data)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async validateVerificationCode(uuid) {
        try {
            const response = await httpService.post(`/verification_codes/${uuid}/verify`)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async confirmVerificationCode(uuid, data) {
        try {
            const response = await httpService.post(`/verification_codes/${uuid}/confirm`, data)
            return response.data
        } catch (error) {
            throw error
        }
    }
}

export const verificationCodesService = new VerificationCodesService()