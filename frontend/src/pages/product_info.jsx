import "react-responsive-carousel/lib/styles/carousel.min.css"; // requires a loader
import { Carousel } from 'react-responsive-carousel';

export default function ProductInfo({mockupImageUrl, aiImageUrl, productTitle, productPrice, productColor, productSizes}){
    return (
        <>
            <div className="product-info-container">
                <div className="carousel-container">
                    <Carousel>
                        <div className="carousel-item">
                            <img src={aiImageUrl} alt="" />
                        </div>
                        <div className="carousel-item">
                            <img src={mockupImageUrl} alt="" />
                        </div>
                    </Carousel>
                </div>
                <div className="product-detail-container">
                    <h1>{productTitle}</h1>
                    <h4>Color: {productColor}</h4>
                    { productSizes.length > 0 && (
                        <div className="size-selection-container">
                            <select name="size-select" id="">
                                {sizes.map((size, index) => (
                                    <option key={index} value={size}>
                                        {size}
                                    </option>
                                ))}
                            </select>
                        </div>
                    )}
                    <h4>Price: {productPrice}€</h4>
                </div>
            </div>
        </>
    )
}