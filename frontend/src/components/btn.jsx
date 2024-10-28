import '../styles/btn.css'
import '../index.css'

export default function Btn({ value, bgColor, textColor, onClick }){
    return (
        <input type="submit" id="submit-btn" onClick={onClick} className="shadow" value={value} style={{"backgroundColor": bgColor, "color": textColor}}/>
    )
}