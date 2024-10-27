import '../styles/product_list.css'
import ProductListCard from '../components/product_list_card'
import Navbar from '../components/navbar'
import Input from '../components/input'
import Btn from '../components/btn'
import { useEffect, useState } from 'react'
import axios from 'axios'
import { useLocation } from 'react-router-dom';


export default function ProductList() {
    const serverUrl = import.meta.env.VITE_SERVER_URL

    const location = useLocation();
    const imageId = location.state?.imageId; // Accessing data from the location state

    const [taskComplete, setTaskComplete] = useState(false);
    const [mockups, setMockups] = useState([])

    // Function to poll task status
    const pollTaskStatus = (imageId) => {
        const interval = setInterval(async () => {
        try {
            // Send GET request to check task status
            const response = await axios.get(serverUrl + '/get-mockup/' + imageId);

            if (response.data.url != null) {
                // Stop polling if task is complete
                const response  = await axios.get(serverUrl + '/get-mockup-by-ai-image-id/' + imageId)
                setMockups(response.data)
                console.log(response.data)
                clearInterval(interval);
                setTaskComplete(true);
            }
        } catch (error) {
            console.error('Error polling task status:', error);
            clearInterval(interval);
            setLoading(false);
        }
        }, 1000); // Poll every second
    };

    useEffect(() => {
        pollTaskStatus(imageId);
    }, []);

    return (
        <>
            <div className="container" style = {{height:"100vh", justifyContent: taskComplete ? "center" : "unset"}}>
                <Navbar name=""/>
                {!taskComplete && (
                    <div className="loading-animation" >
                        <div className="spinner"></div>
                        <h3>Please wait, generating image</h3>
                    </div>
                )}

                {taskComplete && (
                    <div className="loaded-container">
                        <div className="input-again-container">
                            <h1>Dont like the results ? Generate again !</h1>
                            <form action="#" method="POST" className="prompt-form">
                                <Input placeholder={"Enter a prompt for the AI"}/>
                                <div className="btn-index">
                                    <Btn value="GENERATE"/>
                                </div>
                            </form>
                        </div>
                        <hr />
                        <h1 id="product-list-title">Generated products</h1>
                        <div className="product-list-container">
                            {mockups.map((mockup, index) => (
                                <div className="product-list-item">
                                    <ProductListCard imageUrl={mockup.mockup_image_url} productPrice={mockup.price} productTitle={mockup.title}/>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
                
            </div>
            
        </>
    )
}