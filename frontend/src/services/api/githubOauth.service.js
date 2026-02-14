import { httpService } from "./base.service";

class GithubOauthService {
    async getGithubAuthUrl() {
        try {
            return await httpService.get('/oauth/github/url')
        } catch (error) {
            throw error
        }
    }

    async loginGithubUser(code) {
        try {
            const response = await httpService.post('/oauth/github/users/login', code)
            return response.data
        } catch (error) {
            throw error
        }
    }
}

export const githubOauthService = new GithubOauthService()