import React from "react";
import {Link} from "react-router-dom"

function Page2() {

   return (
      <div>
         <p>
            Second Page
         </p>
         <Link to="/">
            <button>
               back
            </button>
         </Link>
      </div>
   )
}

export default Page2;