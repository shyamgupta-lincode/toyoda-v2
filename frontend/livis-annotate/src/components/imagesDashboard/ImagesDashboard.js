import React from 'react'


import Navbar from '../navbar/Navbar'
import './imagesDashboard.css'

export default class ImageDashboard extends React.Component{
constructor(props){
    super(props)
    this.state = {
    images:[],

  }
  }





render(){
return(

<div>
<Navbar/>

<div id="imageThumbnail">
<div className="row">
{
this.props.images.map(function(image) {

         return   <div class="col-md-2">
         <div className="card">
         <div class="card-body">
      <div class="thumbnail">
        <a href={image} target="_blank">
          <img src={image} alt="Lights" id="thumbnail"/>
          {/*<div class="caption">
            <p>Lorem ipsum </p>
          </div>*/}
        </a>
      </div>
    </div>
</div>
</div>
                  })


                  }
 </div>
 </div>

</div>
)

}
}