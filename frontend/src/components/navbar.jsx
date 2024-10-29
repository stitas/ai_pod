import logo from '../assets/logo_crop.png'
import '../styles/navbar.css'
import '../index.css'
import { PersonCircle, Images, BoxArrowInRight, BoxArrowInLeft, Cart } from 'react-bootstrap-icons'
import { useState } from 'react'
import { Squash as Hamburger } from 'hamburger-react'
import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

export default function Navbar() {
    const serverUrl = import.meta.env.VITE_SERVER_URL

    const [isMobileMenuOpen, setMobileMenu] = useState(false)
    const [width, setWidth] = useState(window.innerWidth);
    const [email, setEmail] = useState('')

    const navigate = useNavigate()

    const goToIndex = () => {
        navigate('/')
    }

    const goToGallery = () => {
        navigate('/gallery')
    }

    const goToLogin = () => {
        navigate('/login')
    }

    const goToCart = () => {
        navigate('/cart')
    }

    const goToMyGallery = () => {
        navigate('/my-gallery')
    }

    const logout = async () => {
        try {
            const response = await axios.post(serverUrl + '/logout', {}, {withCredentials: true})

            if(response.status === 200){
                window.location.reload()
            }
        }
        catch (error) {
            console.log(error)
        }
    }

    const getUserEmail = async () => {
        try {
            const response = await axios.get(serverUrl + '/get-user', {withCredentials: true})

            if(response.status == 200){
                setEmail(response.data.email)
                console.log(response.data.email)
            }
            else {
                setEmail('')
            }
        } 
        catch (error){

        }
    }

    useEffect(() => {
        getUserEmail()

        const handleResize = () => setWidth(window.innerWidth);
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, [])

    return (
        <div className='nav-container'>
            <nav className="navbar shadow">
                <div className="burger-nav-list">
                    <a className="nav-logo" onClick={goToIndex}>
                        <img src={logo} alt="" className="logo"/>
                    </a>
                    <Hamburger className="hamburger" toggled={isMobileMenuOpen} toggle={setMobileMenu} />
                </div>

                {/* Regular navbar */}

                <ul className="nav-list">
                    <li className="nav-logo">
                        <a onClick={goToIndex}>
                            <img src={logo} alt="" className="logo"/>
                        </a>
                    </li>
                    <li className="nav-item">
                        <Images color="white" size={25}/>
                        <a className="nav-link" onClick={goToGallery}>Gallery</a>
                    </li>
                    { email === '' ? (
                        <>
                            <li className="nav-item nav-item-right">
                                <Cart color="white" size={25}/>
                                <a className="nav-link" onClick={goToCart}>Cart</a>
                            </li>
                            <li className="nav-item ">
                                <BoxArrowInRight color="white" size={25}/>
                                <a className="nav-link" onClick={goToLogin}>Log In</a>
                            </li>
                        </>
                    ) : (
                        <>
                            <li className="nav-item">
                                <Images color="white" size={25}/>
                                <a className="nav-link" onClick={goToMyGallery}>My Gallery</a>
                            </li>
                            <li className="nav-item nav-item-right">
                                <Cart color="white" size={25}/>
                                <a className="nav-link" onClick={goToCart}>Cart</a>
                            </li>
                            <li className="nav-item">
                                <PersonCircle color="white" size={25}/>
                                <p className="nav-link">{email}</p>
                            </li>
                            <li className="nav-item">
                                <BoxArrowInLeft color="white" size={25}/>
                                <a className="nav-link" onClick={logout}>Logout</a>
                            </li>
                        </>
                    )}
                </ul>
            </nav>
            <div className="burger-dropdown shadow">
                { isMobileMenuOpen && width < 768 ? (
                    <ul className="burger-list">
                        <a className="burger-link" onClick={goToGallery}>
                            <li className="burger-item">
                                Gallery
                            </li>
                        </a>
                        { email === '' ? (
                            <a className="burger-link" onClick={goToLogin}>
                                <li className="burger-item">
                                    Log In
                                </li>
                            </a>
                        ) : (
                            <>
                                <a className="burger-link" onClick={goToMyGallery}>
                                    <li className="burger-item" >
                                        My Gallery
                                    </li>
                                </a>
                                <p className="burger-link">
                                    <li className="burger-item">
                                        {email}
                                    </li>
                                </p>
                                <a className="burger-link">
                                    <li className="burger-item" onClick={logout}>
                                        Logout
                                    </li>
                                </a>
                            </>
                        )}
                    </ul>
                ) : null}
            </div>
        </div>
    )
}