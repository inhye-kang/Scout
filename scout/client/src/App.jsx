import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
// import './App.css'
import axios from "axios";

axios.defaults.baseURL = "http://localhost:8000"
function App() {
  useEffect(() => {
    async function fetch() {
      const response = await axios.post("/hello", {name: "inhye"});
      console.log("response", response.data);
    }
    fetch()
  }, []);
  return (
    <span>hello</span>
  )
}

export default App
