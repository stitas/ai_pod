import logo from '../assets/logo_crop.png'
import '../styles/navbar.css'
import '../App.css'
import { PersonCircle, Images, BoxArrowInRight } from 'react-bootstrap-icons'
import { useState } from 'react'
import { Squash as Hamburger } from 'hamburger-react'
import { useEffect } from 'react'


export default function Navbar({ name }) {
    const [isMobileMenuOpen, setMobileMenu] = useState(false)

    const [width, setWidth] = useState(window.innerWidth);

    useEffect(() => {
        const handleResize = () => setWidth(window.innerWidth);
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, [])

    return (
        <div className='nav-container'>
            <nav className="navbar primary-background">
                <div className="burger-nav-list">
                    <a className="nav-logo" href="#">
                        <img src={logo} alt="" className="logo"/>
                    </a>
                    <Hamburger className="hamburger" toggled={isMobileMenuOpen} toggle={setMobileMenu} />
                </div>

                {/* Regular navbar */}

                <ul className="nav-list">
                    <li className="nav-logo">
                        <a href="#">
                            <img src={logo} alt="" className="logo"/>
                        </a>
                    </li>
                    <li className="nav-item">
                        <a className="nav-link" href="#">About</a>
                    </li>
                    <li className="nav-item">
                        <Images color="white" size={25}/>
                        <a className="nav-link" href="#">Gallery</a>
                    </li>
                    { name === '' ? (
                        <li className="nav-item nav-item-right">
                            <BoxArrowInRight color="white" size={25}/>
                            <a className="nav-link" href="#">Log In</a>
                        </li>
                    ) : (
                        <>
                            <li className="nav-item">
                                <Images color="white" size={25}/>
                                <a className="nav-link" href="#">My Gallery</a>
                            </li>
                            <li className="nav-item nav-item-right">
                                <PersonCircle color="white" size={25}/>
                                <a className="nav-link" href="#">{name}</a>
                            </li>
                        </>
                    )}
                </ul>
            </nav>
            <div className="burger-dropdown">
                { isMobileMenuOpen && width < 768 ? (
                    <ul className="burger-list">
                        <li className="burger-item solid-border-primary-darker primary-background">
                            <a className="burger-link" href="#">About</a>
                        </li>
                        <li className="burger-item solid-border-primary-darker primary-background ">
                            <a className="burger-link" href="#">Gallery</a>
                        </li>
                        { name === '' ? (
                            <li className="burger-item solid-border-primary-darker primary-background ">
                                <a className="burger-link" href="#">Log In</a>
                                
                            </li>
                        ) : (
                            <>
                                <a className="burger-link" href="#">
                                    <li className="burger-item solid-border-primary-darker primary-background ">
                                        My Gallery
                                    </li>
                                </a>
                                <li className="burger-item solid-border-primary-darker primary-background ">
                                    <a className="burger-link" href="#">{name}</a>
                                </li>
                            </>
                        )}
                    </ul>
                ) : null}
            </div>
        </div>
    )
}