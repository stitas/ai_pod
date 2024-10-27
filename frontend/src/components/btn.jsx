import '../styles/btn.css'
import '../index.css'

export default function Btn({ value, bgColor, textColor }){
    return (
        <input type="submit" id="submit-btn" className="shadow" value={value} style={{"backgroundColor": bgColor, "color": textColor}}/>
    )
}