import './App.css'
import Navbar from './components/navbar'
import Input from './components/input'
import Btn from './components/btn'
import ai_robot_about from './assets/ai_robot_about.png'  
import { useContext, useState } from 'react'
import { useNavigate } from 'react-router-dom';
import axios from 'axios'
import { UserContext } from './contexts/user_context'

export default function App() {
  const navigate = useNavigate()

  const serverUrl = import.meta.env.VITE_SERVER_URL

  const { isLoggedIn } = useContext(UserContext)

  const [inputText, setInputText] = useState('')

  const goToRegister = () => {
    navigate('/register')
  }

  const goToLogin = () => {
    navigate('/login')
  }

  // Function to start the task
  const startTask = async (event) => {
    event.preventDefault()

    try {
        const data = {
          prompt: inputText,
        }

        // Send POST request to start the task
        const response = await axios.post(
          serverUrl + '/mockup-generator/create-task', data, {withCredentials: true}
        );

        console.log(response.data)

        if(response.status == 401){
          navigate('/login')
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
        // If not authenticated redirect to login
        console.error('Error starting task:', error);
    }
  };

  const handleInputChange = (event) => {
    setInputText(event.target.value);
  };

  return (
    <>
      <div className="container gradient">
        <div className="main-container">
          <Navbar/>
          <div className="index-container">
            <h1 id="index-title">Let your imagination flow...</h1>
            <h3 id="title-lower">Just relax. The AI will do all the work for you.</h3>
            <form action="#" onSubmit={isLoggedIn ? startTask : goToLogin} method="POST" className="prompt-form">
              <Input placeholder={"Enter a prompt for the AI"} onChange={handleInputChange}/>
              <div className="btn-index">
                <Btn value="GENERATE"/>
              </div>
            </form>
          </div>
        </div>
        <div className="about-container">
          <div className="about-text">
            <h1 id="about-title">About AIPOD</h1>
            <p id="about-desc">   
              Welcome to AI Impressions, where creativity meets cutting-edge technology! 
            </p>
            <br />
            <p id="about-desc">
              At <b>AIPOD</b>, we offer a unique experience that allows you to turn your imagination into reality. 
            </p>
            <br />
            <p id="about-desc">
                Using our state-of-the-art AI image generator, you can simply input your ideas, and our AI will create stunning, custom images tailored just for you.
            </p>
            <br />
            <p id="about-desc">
              But it doesn't stop there. Once you've generated the perfect image, we make it easy for you to bring it into your life. 
            </p>
            <br />
            <p id="about-desc">
            Whether you're looking for unique apparel, personalized mugs, canvas prints, or other custom products, we've got you covered. 
            Our seamless process allows you to choose from a variety of high-quality products and have your custom AI-generated design printed directly on them.
            </p>
          </div>
          <div className="about-image">
            <img id="about-robot-img" src={ai_robot_about}/>
          </div>
        </div>
        <div className="how-it-works-container">
          <div className="how-it-works-title">
            <h1 id="how-it-works-title">How it all works</h1>
          </div>
          <div className="how-it-works-card-container">
            <div className="how-it-works-card shadow">
              <h2 id="how-it-works-card-title">Create Your Vision</h2>
              <p id="how-it-works-card-desc">Start by describing your vision to our AI. Whether it's a landscape, a quirky abstract, or a creative mashup, our AI will generate a beautiful, high-resolution image just for you.</p>
            </div>
            <div className="how-it-works-card shadow">
              <h2 id="how-it-works-card-title">Customize Your Product</h2>
              <p id="how-it-works-card-desc">Once you're happy with the design, you can choose from a wide range of products—t-shirts, hoodies, mugs, posters, and more.</p>
            </div>
            <div className="how-it-works-card shadow">
              <h2 id="how-it-works-card-title">High Quality Prints</h2>
              <p id="how-it-works-card-desc">We ensure that each product is printed with care, using high-quality materials and the latest printing techniques to bring your AI-generated artwork to life.</p>
            </div>
            <div className="how-it-works-card shadow">
              <h2 id="how-it-works-card-title">Delivered to Your Doorstep</h2>
              <p id="how-it-works-card-desc">After selecting your product, simply place your order, and we’ll take care of the rest. Your unique design will be shipped straight to your doorstep!</p>
            </div>
          </div>
          <div className="try-btn">
            <Btn value="TRY IT OUT" bgColor="white" textColor="black" hoverColor="gray" onClick={goToRegister}/>
          </div>
        </div>
      </div>
      
    </>
  )
}
