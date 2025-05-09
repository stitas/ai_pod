import { useLocation, useNavigate } from "react-router-dom"
import axios from 'axios'
import { useEffect, useContext } from 'react'
import { UserContext } from '../contexts/user_context'

export default function AuthenticateWait() {
    const { login } = useContext(UserContext)
    const location = useLocation()
    const navigate = useNavigate()
    const queryParams = new URLSearchParams(location.search)
    const serverUrl = import.meta.env.VITE_SERVER_URL

    const authCode = queryParams.get('code')
    const error = queryParams.get('error')

    const authenticateGoogle = async () =>{
        try {
            const data = {
                authorization_code: authCode
            }

            if(error){
                navigate('/login', 
                    {
                        state: {googleError: 'Failed to authenticate with google'}
                    }
                )
            }

            const response = await axios.post(serverUrl + '/authorize-google', data, {withCredentials: true})
            
            if(response.status === 200){
                const userData = await getUser()
                login(userData)
                navigate('/')
            }
            else {
                navigate('/login', 
                    {
                        state: {googleError: 'Failed to authenticate with google'}
                    }
                )
            }
        }   
        catch (error){
            console.log(error)
        }
    }

    const getUser = async () => {
        try {
            const response = await axios.get(serverUrl + '/get-user', {withCredentials: true})
    
            if(response.status == 200){
              return response.data
            }
    
        } 
        catch (error){
          console.log(error)
        }
    } 


    useEffect(() => {
        authenticateGoogle();
    }, []);

    return (
        <>
            <div className="container" style={{height: "100vh"}}>
                <div className="loading-animation" style={{marginTop: "0rem"}}>
                    <div className="spinner"></div>
                    <h3 style={{color: "white", fontWeight: "bold", fontSize:"2rem"}}>Please wait authenticating...</h3>
                </div>
            </div>
        </>
    )
}