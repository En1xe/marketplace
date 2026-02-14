import { useEffect } from 'react'
import {useSearchParams} from 'react-router-dom'

import { githubOauthService } from '@services/api/githubOauth.service'


export default function GitHub() {
    const [params, _] = useSearchParams()

    useEffect(() => {
        const code = params.get('code')

        const loginUser = async () => {
            const response = await githubOauthService.loginGithubUser({code})

            if (response) {
                const access_token = response.access_token
                localStorage.setItem('access', access_token)

                window.location.href = '/'
            }

        }

        return loginUser
    }, [])
 
    return (
        <>
        </>
    )
}