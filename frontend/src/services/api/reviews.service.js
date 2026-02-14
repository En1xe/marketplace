import { httpService } from "./base.service";


class ReviewsService {
    async getReviews(...filters) {
        try {
            const params = new URLSearchParams()

            for (const [key, value] of Object.entries(...filters)) {
                params.append(key, value)
            }
            const queryString = params.toString()

            const response = await httpService.get(`/reviews?${queryString}`)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async getReview(uuid) {
        try {
            const response = await httpService.get(`/reviews/${uuid}`)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async createReview(data) {
        try {
            const response = await httpService.post('/reviews', data)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async updateReview(uuid, data) {
        try {
            const response = await httpService.patch(`/reviews/${uuid}`, data)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async deleteReview(uuid) {
        try {
            const response = await httpService.delete(`/reviews/${uuid}`)
            return response.data
        } catch (error) {
            throw error
        }
    }
}

export const reviewsService = new ReviewsService()