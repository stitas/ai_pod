import '../styles/input_auth.css'
import '../index.css'

export default function InputAuth( {placeholder, type, onChange} ){
    return (
        <input type={type} className="input-auth shadow" placeholder={placeholder} onChange={onChange}/>
    )
}