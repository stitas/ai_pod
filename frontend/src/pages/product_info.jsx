import 'react-responsive-carousel/lib/styles/carousel.min.css'; // requires a loader
import { Carousel } from 'react-responsive-carousel';
import { useLocation } from 'react-router-dom';
import '../styles/product_info.css'
import Navbar from '../components/navbar';
import Btn from '../components/btn';
import { useContext, useEffect, useState } from 'react';
import { UserContext } from '../contexts/user_context';

export default function ProductInfo(){
    const location = useLocation();
    const mockup = location.state?.mockup; // Accessing data from the location state
    const aiImageUrl = location.state?.aiImageUrl

    const sizes = ['S', 'M', 'L', 'XL']

    const { isLoggedIn } = useContext(UserContext)

    const addToCart = () => {
        if(isLoggedIn){

        }
        else {
            
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
                                <img src={aiImageUrl} alt="" />
                            </div>
                            <div className="carousel-item">
                                <img src={mockup.mockup_image_url} alt="" />
                            </div>
                        </Carousel>
                    </div>
                    <div className="product-detail-container">
                        <div className="product-info-title-container">
                            <h1 id="product-info-title">{mockup.title}</h1>
                        </div>
                        <div className="product-specs-container">
                            <div className="products-spec">
                                <p id="product-info-text">Color | {mockup.color}</p>
                            </div>
                            {/* If not tote bag */}
                            <div className="products-spec">
                                { mockup.printful_product_id != 367 && mockup.printful_product_id != 19 && (
                                    <div className="size-selection-container">
                                        <p id="product-info-text">Select a size:</p>
                                        <select id="size-select" name="size-select">
                                            {sizes.map((size, index) => (
                                                <option key={index} value={size}>
                                                    {size}
                                                </option>
                                            ))}
                                        </select>
                                    </div>
                                )}
                            </div>
                            <div className="products-spec">
                                <p id="product-info-text">Select quantity:</p>
                                <input id="quantity-select" type="number" min={1}/>
                            </div>
                            <div className="products-spec">
                                <p id="product-info-text">Price: <s>{(mockup.price * 1.2).toFixed(2)}€</s> {mockup.price}€</p>
                            </div>
                        </div>
                        <div className="add-to-cart-btn-container">
                            <Btn value={"ADD TO CART"} onClick={addToCart}/>
                        </div>
                    </div>
                </div>
            </div>
        </>
    )
}