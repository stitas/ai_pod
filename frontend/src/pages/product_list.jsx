import '../styles/product_list.css'
import ProductListCard from '../components/product_list_card'
import Navbar from '../components/navbar'
import Input from '../components/input'
import Btn from '../components/btn'
import { useContext, useEffect, useState } from 'react'
import axios from 'axios'
import { useLocation, useNavigate } from 'react-router-dom';
import { UserContext } from '../contexts/user_context'


export default function ProductList() {
    const serverUrl = import.meta.env.VITE_SERVER_URL

    const { isLoggedIn } = useContext(UserContext)

    const navigate = useNavigate()
    const location = useLocation();
    const imageId = location.state?.imageId; // Accessing data from the location state

    const [taskComplete, setTaskComplete] = useState(false);
    const [mockups, setMockups] = useState([])
    const [inputText, setInputText] = useState('')
    const [aiImageUrl, setAiImageUrl] = useState('')

    // Function to poll task status
    const pollTaskStatus = (imageId) => {
        const interval = setInterval(async () => {
        try {
            // Send GET request to check task status
            const response = await axios.get(serverUrl + '/get-image/' + imageId);

            if (response.data.url != null) {
                // Stop polling if task is complete
                setAiImageUrl(response.data.url)
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

    const getMockups = async (imageId) => {
        if(taskComplete) {
            axios.get(serverUrl + '/get-mockups-by-ai-image-id/' + imageId)
            .then((response) => {
                setMockups(response.data);
            })
            .catch((error) => {
                console.error('Error fetching mockups:', error);
            });
        }
    }

    // Function to start the task
    const startTask = async (event) => {
        event.preventDefault()

        try {
            const data = {
                prompt: inputText,
            }

            // Send POST request to start the task
            const response = await axios.post(serverUrl + '/mockup-generator/create-task', data, {withCredentials: true});
            response.data.image_id 

            // If not authenticated redirect to login
            if(response.status === 401){
                navigate(
                '/login'
                )
            }
            else {
                navigate(
                '/product-list',
                {
                    state: { imageId: response.data.image_id  },
                }
                ); 
            }
        } 
        catch (error) {
            console.error('Error starting task:', error);
        }
    };

    const handleInputChange = (event) => {
        setInputText(event.target.value);
    };

    const goToProductInfo = (mockup) => {
        navigate(
            '/product-info',
            {
                state: { mockup: mockup, aiImageUrl: aiImageUrl},
            }
        );
    }

    const goToLogin = () => {
        navigate(
            '/login',
        );
    }

    useEffect(() => {
        getMockups(imageId);
    }, [taskComplete]);

    useEffect(() => {
        pollTaskStatus(imageId);
    }, []);

    return (
        <>
            <div className="container" style = {{height: taskComplete ? "100%" : "100vh", justifyContent: taskComplete ? "center" : "unset"}}>
                <Navbar/>
                {!taskComplete && (
                    <div className="loading-animation" >
                        <div className="spinner"></div>
                        <h3 style={{color: "black", fontWeight: "bold", fontSize:"2rem"}}>Please wait, generating image...</h3>
                    </div>
                )}

                {taskComplete && (
                    <div className="loaded-container">
                        <div className="input-again-container">
                            <h1>Dont like the results ? Generate again !</h1>
                            <form onSubmit={isLoggedIn ? startTask : goToLogin} method="POST" className="prompt-form">
                                <Input placeholder={"Enter a prompt for the AI"} onChange={handleInputChange}/>
                                <div className="btn-index">
                                    <Btn value="GENERATE"/>
                                </div>
                            </form>
                        </div>
                        <hr />
                        <h1 id="product-list-title">Generated products</h1>
                        <div className="product-list-container">
                            {mockups.map((mockup, index) => (
                                <div key={index} className="product-list-item" onClick={() => {goToProductInfo(mockup)}}>
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