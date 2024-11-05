import Btn from "../components/btn"
import { useNavigate } from "react-router-dom"
import { CartContext } from "../contexts/cart_context"
import axios from "axios"
import { useContext } from "react"
import { UserContext } from "../contexts/user_context"

export default function Pay() {
    const navigate = useNavigate()
    const { clearCart, cartSum, cart } = useContext(CartContext)
    const serverUrl = import.meta.env.VITE_SERVER_URL;
    const { isLoggedIn } = useContext(UserContext)

    const clearCartDb = async () =>{
        try {
            await axios.post(serverUrl + '/clear-cart', {}, {withCredentials: true})
        }
        catch (error){
            console.log(error)
        }
    }

    const onPay = () => {
        const state = {
            cart: cart,
            cart_sum: cartSum
        }

        clearCart()
        if(isLoggedIn){
            clearCartDb()
        }
        navigate('/thank-you', 
            {
                state: state
            }
        )
    }

    return (
        <>
            <div className="container">
                <Btn value={"PAY"} onClick={onPay}/>
            </div>
        </>
    )
}