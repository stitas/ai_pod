import 'react-responsive-carousel/lib/styles/carousel.min.css'; // requires a loader
import { Carousel } from 'react-responsive-carousel';
import { useLocation } from 'react-router-dom';
import '../styles/product_info.css'
import Navbar from '../components/navbar';
import Btn from '../components/btn';
import { useContext, useEffect, useState } from 'react';
import { UserContext } from '../contexts/user_context';
import { CartContext } from '../contexts/cart_context';
import axios from 'axios';

export default function ProductInfo(){
    const location = useLocation();
    let mockup = location.state?.mockup; // Accessing data from the location state
    const aiImageUrl = location.state?.aiImageUrl
    const serverUrl = import.meta.env.VITE_SERVER_URL

    const sizes = ['S', 'M', 'L', 'XL']

    const { isLoggedIn } = useContext(UserContext)
    const { addToCart, cart } = useContext(CartContext)

    const[selectedSize, setSelectedSize] = useState('S')

    const handleSizeChange = (event) => {
        setSelectedSize(event.target.value)
    }

    const addItem = async () => {
        if(isLoggedIn){
            try {
                const check_data = {
                    mockup_id: mockup.id,
                    size: selectedSize
                }

                const exists = await axios.post(serverUrl + '/check-cart-item-exists/' + mockup.id, check_data, {withCredentials: true})
                const quantity = exists.data.quantity

                if(exists.status === 200){
                    const data = {
                        mockup_id: mockup.id,
                        quantity: quantity + 1,
                        size: selectedSize
                    }

                    axios.post(serverUrl + '/update-cart-item', data, {withCredentials: true})
                }
            }
            catch (error) {
                const data = {
                    mockup_id: mockup.id,
                    size: selectedSize
                }

                axios.post(serverUrl + '/create-cart-item', data, {withCredentials: true})
            }
        }
        else {
            mockup = {...mockup, size: selectedSize}
            addToCart(mockup)
        }
    }

    return (
        <>  
            <div className="container">
                <Navbar/>
                <div className="product-info-container">
                    <div className="carousel-container">
                        <Carousel>
                            <div className="carousel-item">
                                <img src={aiImageUrl} alt="AI generated image" />
                            </div>
                            <div className="carousel-item">
                                <img src={mockup.mockup_image_url} alt="Product mockup image" />
                            </div>
                        </Carousel>
                    </div>
                    <div className="product-detail-container">
                        <h1 className="product-title">{mockup.title}</h1>
                        <div className="product-specs">
                            <div className="product-spec">
                                <p><strong>Color:</strong> {mockup.color}</p>
                            </div>
                            {mockup.printful_product_id !== 367 && mockup.printful_product_id !== 19 && (
                                <div className="product-spec">
                                    <p><strong>Select a size:</strong></p>
                                    <select id="size-select" name="size-select" onChange={handleSizeChange}>
                                        {sizes.map((size, index) => (
                                            <option key={index} value={size}>
                                                {size}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            )}
                            <div className="product-spec price">
                                <p>
                                    <strong>Price:</strong> <s>{(mockup.price * 1.2).toFixed(2)}€</s> {mockup.price}€
                                </p>
                            </div>
                        </div>
                        <div className="add-to-cart-btn-container">
                            <Btn value="ADD TO CART" onClick={addItem} />
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}