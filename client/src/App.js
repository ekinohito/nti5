import './App.css';
import {HomePage} from "./pages/home/HomePage";
import React from "react";
import {useDispatch} from "react-redux";
import {fetchUser} from "./actions";

function App() {
    const dispatch = useDispatch();
    if (localStorage.getItem('token'))
        dispatch(fetchUser())
  return (
    <div className="App">
      <HomePage/>
    </div>
  );
}

export default App;
