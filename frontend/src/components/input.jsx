import '../styles/input.css'
import '../index.css'

export default function Input( {placeholder, onChange} ){
    return (
        <input type="text" id="input" placeholder={placeholder} className="shadow" onChange={onChange}/>
    )
}