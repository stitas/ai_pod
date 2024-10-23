import '../styles/input.css'
import '../index.css'

export default function Input( {placeholder} ){
    return (
        <input type="text" id="input" placeholder={placeholder}/>
    )
}