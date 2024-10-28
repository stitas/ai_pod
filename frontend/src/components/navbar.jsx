import logo from '../assets/logo_crop.png'
import '../styles/navbar.css'
import '../index.css'
import { PersonCircle, Images, BoxArrowInRight, Cart } from 'react-bootstrap-icons'
import { useState } from 'react'
import { Squash as Hamburger } from 'hamburger-react'
import { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

export default function Navbar({ name }) {
    const [isMobileMenuOpen, setMobileMenu] = useState(false)

    const [width, setWidth] = useState(window.innerWidth);

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

    useEffect(() => {
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
                    { name === '' ? (
                        <>
                            <li className="nav-item nav-item-right">
                                <Cart color="white" size={25}/>
                                <a className="nav-link" onClick={goToCart}>Cart</a>
                            </li>
                            <li className="nav-item ">
                                <BoxArrowInRight color="white" size={25}/>
                                <a className="nav-link" href="#" onClick={goToLogin}>Log In</a>
                            </li>
                        </>
                    ) : (
                        <>
                            <li className="nav-item">
                                <Images color="white" size={25}/>
                                <a className="nav-link" href="#">My Gallery</a>
                            </li>
                            <li className="nav-item nav-item-right">
                                <Cart color="white" size={25}/>
                                <a className="nav-link" onClick={goToCart}>Cart</a>
                            </li>
                            <li className="nav-item">
                                <PersonCircle color="white" size={25}/>
                                <a className="nav-link" href="#">{name}</a>
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
                        { name === '' ? (
                            <a className="burger-link" onClick={goToLogin}>
                                <li className="burger-item">
                                    Log In
                                </li>
                            </a>
                        ) : (
                            <>
                                <a className="burger-link" href="#">
                                    <li className="burger-item">
                                        My Gallery
                                    </li>
                                </a>
                                <a className="burger-link" href="#">
                                    <li className="burger-item">
                                        {name}
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