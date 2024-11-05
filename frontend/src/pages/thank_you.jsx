import Btn from "../components/btn"
import { useNavigate, useLocation } from "react-router-dom"
import '../styles/thank_you.css'
import { useContext, useEffect, useState } from "react"
import axios from "axios"
import { UserContext } from "../contexts/user_context"

export default function ThankYou(){
    const navigate = useNavigate()
    const serverUrl = import.meta.env.VITE_SERVER_URL;
    const { isLoggedIn, user } = useContext(UserContext)
    const location = useLocation();

    const [orderText, setOrderText] = useState('')

    const createOrder = async () => {
        try {
            const data = {
                user_id: isLoggedIn ? user.id : null,
                order_price: location.state?.cart_sum,
                cart: location.state?.cart
            }

            await axios.post(serverUrl + '/create-order', data)

            setOrderText('Thank you for your order')
        }
        catch (error) {
            console.log(error)
            setOrderText('Something went wrong')
        }
    }

    const goToIndex = () => {
        navigate('/')
    }

    useEffect(() => {
        createOrder()
    }, [])

    return (
        <>
        <div className="container">
            <div className="thank-you-items-container">
                <h1>{orderText}</h1>
                <Btn value={"Return to home"} onClick={goToIndex}/>
            </div>
        </div>
        </>
    )
}