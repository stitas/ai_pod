import InputAuth from '../components/input_auth'
import Btn from '../components/btn'
import '../styles/login.css'
import { useNavigate, useLocation } from 'react-router-dom'
import { useEffect, useState } from 'react'
import axios from 'axios'

export default function Login() {
    const location = useLocation();
    const navigate = useNavigate()
    const serverUrl = import.meta.env.VITE_SERVER_URL
    const googleError = location.state?.googleError; // Accessing data from the location state

    console.log(googleError)

    const[email, setEmail] = useState('')
    const[password, setPassword] = useState('')
    const[loginError, setLoginError] = useState('')

    const login = async (event) => {
        event.preventDefault()

        try {
            const data = {
                email: email,
                password: password
            }
    
            const response = await axios.post(serverUrl + '/login', data)
    
            // check invalid credentials
            if(response.status === 401){
                setLoginError('Invalid credentials')
            }
            else {
                navigate('/')
            }
        }
        catch(error) {
            console.error('Error starting task:', error);
        }
    }

    const loginGoogle = async () => {
        try {
            const response = await axios.get(serverUrl + '/login-google')

            if(response.status === 200){
                window.location.replace(response.data.redirect_url);
            }
        }
        catch(error) {
            console.error('Error starting task:', error);
        }
    }


    const handleInputEmail = (event) => {
        setEmail(event.target.value)
    }

    const handleInputPassword = (event) => {
        setPassword(event.target.value)
    }

    const goToRegister = () => {
        navigate('/register')
    }

    useEffect(() => {
        setLoginError(googleError)
    }, [])

    return (
        <div className="container" style = {{height:"100vh"}}>
            <div className="login-container shadow">
                <h1>Login</h1>
                <form method="post" className="login-form" onSubmit={login}>
                    <InputAuth placeholder={"Enter email"} type={"text"} onChange={handleInputEmail}/>
                    <InputAuth placeholder={"Enter password"} type={"password"} onChange={handleInputPassword}/>
                    <div className="login-btn">
                        <Btn value={"Login"}/>
                    </div>
                </form>
                <hr />  
                <div className="google-login-container">
                    <a id="google-anchor" onClick={loginGoogle}>
                        <div className="google-login-btn shadow">
                            <div id="google-logo">
                                <svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="50" height="50" viewBox="0 0 48 48">
                                    <path fill="#FFC107" d="M43.611,20.083H42V20H24v8h11.303c-1.649,4.657-6.08,8-11.303,8c-6.627,0-12-5.373-12-12c0-6.627,5.373-12,12-12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C12.955,4,4,12.955,4,24c0,11.045,8.955,20,20,20c11.045,0,20-8.955,20-20C44,22.659,43.862,21.35,43.611,20.083z"></path><path fill="#FF3D00" d="M6.306,14.691l6.571,4.819C14.655,15.108,18.961,12,24,12c3.059,0,5.842,1.154,7.961,3.039l5.657-5.657C34.046,6.053,29.268,4,24,4C16.318,4,9.656,8.337,6.306,14.691z"></path><path fill="#4CAF50" d="M24,44c5.166,0,9.86-1.977,13.409-5.192l-6.19-5.238C29.211,35.091,26.715,36,24,36c-5.202,0-9.619-3.317-11.283-7.946l-6.522,5.025C9.505,39.556,16.227,44,24,44z"></path><path fill="#1976D2" d="M43.611,20.083H42V20H24v8h11.303c-0.792,2.237-2.231,4.166-4.087,5.571c0.001-0.001,0.002-0.001,0.003-0.002l6.19,5.238C36.971,39.205,44,34,44,24C44,22.659,43.862,21.35,43.611,20.083z"></path>
                                </svg>
                            </div>
                            <h5>Login with google</h5>
                        </div>
                    </a>
                </div>
                <div className="register-anchor">
                    <a onClick={goToRegister}> Dont have an account ? Sign up!</a>
                </div>
                <div className="form-error">
                    <p style={{color: "red"}}>{loginError}</p>
                </div>
            </div>
        </div>
    )
}