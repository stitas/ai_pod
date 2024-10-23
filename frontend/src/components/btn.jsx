import '../styles/btn.css'
import '../index.css'

export default function Btn({ value }){
    return (
        <input type="submit" id="submit-btn" className="primary-background" value={value}/>
    )
}