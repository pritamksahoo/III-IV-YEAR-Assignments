import auth0 from 'auth0-js';
import history from './history';

class Auth {
    authentication = new auth0.WebAuth({
        domain: 'pritamksahoo.auth0.com',
        clientID: '4chQTy7MB3iR4Q6sEPGhLZHVwTC5q2oY',
        redirectUri: 'http://localhost:3000/callback',
        responseType: 'token id_token',
        scope: 'openid profile email'
    })

    login = () => {
        this.authentication.authorize()
    }

    handleAuthentication = () => {
        this.authentication.parseHash((err, result) => {
            if (result) {
                localStorage.setItem('access_token', result.accessToken)
                localStorage.setItem('id_token', result.idToken)
                
                let expiresAt = JSON.stringify(new Date().getTime() + result.expiresIn * 1000)
                localStorage.setItem('expiresAt', expiresAt)

                setTimeout(() => {
                    history.replace("authcheck")
                }, 200)
            } else {
                console.log(err)
            }
        })
    }

    handleLogOut = () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('id_token')
        localStorage.removeItem('expiresAt')
    }

    isAuthenticated = () =>  {
        let exp = JSON.parse(localStorage.getItem('expiresAt'))

        return new Date().getTime() < exp
    }
}

export default Auth;