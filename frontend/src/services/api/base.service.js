import axios from "axios"

const API_BASE_URL = 'http://localhost:8000'

class HttpService {
    constructor() {
        this.client = axios.create({
            baseURL: API_BASE_URL,
            withCredentials: true,
            headers: {
                'Content-Type': 'application/json',
            },
        })

        this.setupInterceptors()
    }

    setupInterceptors() {
        this.client.interceptors.request.use(
            (config) => {
                const token = localStorage.getItem('access')

                if (token) {
                    config.headers.Authorization = `Bearer ${token}`
                }

                return config
            },
            (error) => Promise.reject(error)
        )

        this.client.interceptors.response.use(
            (response) => response,
            async (error) => {
                if (!error.response) {
                    return Promise.reject(new Error('No response'))
                }

                const originalRequest = error.config
                
                if (
                    error.response.status === 401
                    && !originalRequest._retry
                ) {
                    try {
                        const response = await axios.get(
                            `${API_BASE_URL}/auth/tokens`, 
                            {
                                withCredentials: true
                            }
                        )
                        const token = response.data?.access_token

                        if (token) {
                            localStorage.setItem('access', token)
                        } else {
                            return 
                        }

                        originalRequest._retry = true

                        return this.client(originalRequest)
                    } catch (error) {
                        Promise.reject(error)
                    }
                }

                return Promise.reject(error)
            }
        )
    }

    get(url, config={}) {
        return this.client.get(url, config)
    }

    post(url, data, config={}) {
        return this.client.post(url, data, config)  
    }

    patch(url, data, config={}) {
        return this.client.patch(url, data, config)
    }

    delete(url, data, config={}) {
        return this.client.delete(url, data, config)
    }
}

export const httpService = new HttpService()