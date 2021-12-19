import React from "react";
import {Link} from "react-router-dom"
import "./styles.css"

function results() {
   return (
      <div>
         <section>
            <Link to="/">
               <button type="submit">Back</button>
            </Link>
         </section>
      </div>
   )
}

export default results;