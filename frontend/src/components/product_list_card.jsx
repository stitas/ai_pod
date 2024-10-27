import '../styles/product_list_card.css'

export default function ProductListCard( {imageUrl, productTitle, productPrice} ) {
    return (
        <div className="product-card shadow">
            <img src={imageUrl} alt="" id="product-image"/>
            <div className="product-info">
                <h3>{productTitle}</h3>
                <p>{productPrice}€</p>
            </div>
        </div>
    )
}