
import React from "react";
import { Link } from "react-router-dom";

function App() {
  return (
    <div className='App' align='center'>
       <h1>Playlist Builder</h1>
       <Link to='/page2'>
          <button className='btn'>change page</button>
          </Link>
    </div>
  )
}

export default App;
