import '../styles/input_auth.css'
import '../index.css'

export default function InputAuth( {placeholder, type} ){
    return (
        <input type={type} id="input-auth" placeholder={placeholder} className="shadow"/>
    )
}