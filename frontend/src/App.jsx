import './App.css'
import './styles/navbar.css'
import Navbar from './components/navbar'
import Input from './components/input'
import Btn from './components/btn'

export default function App() {
  return (
    <>
      <Navbar name="titas" />
      <div className="main-container">
        <h1 id="index-title">Let your imagination flow...</h1>
        <h3 id="title-lower">Just relax. The AI will do all the work for you.</h3>
        <form action="#" method="POST" className="prompt-form">
          <Input placeholder={"Enter a prompt for the AI"}/>
          <Btn value="GENERATE"/>
        </form>
      </div>
    </>
  )
}
