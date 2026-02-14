import { httpService } from "./base.service";


class ListingsService {
    async getListings(...filters) {
        try {
            const params = new URLSearchParams()

            for (const [key, value] of Object.entries(...filters)) {
                params.append(key, value)
            }
            const queryString = params.toString()

            const response = await httpService.get(`/listings?${queryString}`)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async getListing(uuid) {
        try {
            const response = await httpService.get(`/listings/${uuid}`)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async createListing(data) {
        try {
            const response = await httpService.post('/listings', data)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async updateListing(uuid, data) {
        try {
            const response = await httpService.patch(`/listings/${uuid}`, data)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async deleteListing(uuid) {
        try {
            const response = await httpService.delete(`/listings/${uuid}`)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async createListingMedia(data) {
        try {
            const response = await httpService.post('/listings/media', data, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })
            return response.data
        } catch (error) {
            throw error
        }
    }

    async updateListingMedia(data) {
        try {
            const response = await httpService.patch('/listings/media', data, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            })

            return response.data
        } catch (error) {
            throw error
        }
    }

    async getListingFavorite(filters = {}) {
        try {
            const params = new URLSearchParams()

            for (const [key, value] of Object.entries(filters)) {
                params.append(key, value)
            }
            
            const queryString = params.toString()

            const response = await httpService.get(`/listings/favorite?${queryString}`)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async createListingFavorite(data) {
        try {
            const response = await httpService.post('/listings/favorite', data)
            return response.data
        } catch (error) {
            throw error
        }
    }

    async deleteListingFavorite(listingId) {
        try {
            const response = await httpService.delete(`/listings/favorite/${listingId}`)

            return response.data
        } catch (error) {
            throw error
        }
    }

    async createListingView(data) {
        try {
            const response = await httpService.post('/listings/views', data)
            return response.data
        } catch (error) {
            throw error
        }
    }
}

export const listingsService = new ListingsService()