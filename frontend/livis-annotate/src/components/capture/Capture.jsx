import React from 'react'
// import { BrowserRouter as Router, Route, Link, Switch, useParams } from "react-router-dom"
import Navbar from '../navbar/Navbar'
import axios from 'axios'
import {
  
    Modal,
 
    } from "reactstrap";
import Pagination from "react-js-pagination";
import { ToastContainer, toast } from 'react-toastify';
export default class Capture extends React.Component{
    

    constructor(props){
        super(props)
        this.state = {
            showUploadModal:false,
            file:'Choose File',
            upload_button_text:'Upload',
            selectedFile:null,
            part_id:null,
            part_images:null,
            activePage:1,
            per_page:20,
            parts:[],
            img_url:null,
       }
    }

    // window.addEventListener("beforeunload", function (e) {
    //     var confirmationMessage = "\o/";
      
    //     (e || window.event).returnValue = confirmationMessage; //Gecko + IE
    //     return confirmationMessage;                            //Webkit, Safari, Chrome
    //   });
componentWillUnmount() {
    alert("DSdf");
      console.log("dadfs");
 }
 componentDidMount() {
    //  this.startCamera();
     this.getParts();
   

 }

 startCamera = async () => {
    await axios.get(window.$livis_config.API_URL+"start_capture_camera/")
    .then(response => {
        this.getImageUrl();
       // alert("ds");
    // //    console.log(typeof response);
    //   if (response != false) {
    //        this.setState({img_url:response.data})
    //     //    console.log(this.state.part_images);
    //   }
    })
    .catch((error) => {
      console.log(error);
    })
  };

  stopCamera = async () => {
    await axios.get(window.$livis_config.API_URL+"stop_capture_camera/")
    .then(response => {
       // alert("ds");
    // //    console.log(typeof response);
    //   if (response != false) {
    //        this.setState({img_url:response.data})
    //     //    console.log(this.state.part_images);
    //   }
    })
    .catch((error) => {
      console.log(error);
    })
  };



 getImageUrl = async () => {
    await axios.get(window.$livis_config.API_URL+"get_capture_feed_url/")
    .then(response => {
       // alert("ds");
    //    console.log(typeof response);
      if (response != false) {
           this.setState({img_url:response.data.capture_url})
        //    console.log(this.state.part_images);
      }
    })
    .catch((error) => {
      console.log(error);
    })
  };



 getParts = async () => {
    await axios.get(`http://164.52.194.78:8000/livis/v1/parts/get_all_parts/`)
    .then(response => {
       // alert("ds");
    //    console.log(typeof response);
      if (response != false) {
           this.setState({parts:response.data})
        //    console.log(this.state.part_images);
      }
    })
    .catch((error) => {
      console.log(error);
    })
  };


    
captureImage()
{
    
    if(this.state.part_id !== null)
    {
        axios.post(window.$livis_config.API_URL+"capture_part_image/",{part_id:this.state.part_id}
        ).then(res => { 
          // console.log(res);
         toast.success("Saved Successfully");
        }).catch((error) => {
          toast.error("Unknown Error");
        })
    }else{
        toast.error("Please select part id");
    }

}

onChangePartNumber = (event)=> {
    const selectedIndex = event.target.options.selectedIndex;
    var part_id = (event.target.options[selectedIndex].getAttribute('data-key'))
    console.log(part_id);
    this.setState({part_id:part_id})
    // console.log(part_id);
}

   
    render(){
   

        return(
        <>
         <ToastContainer />
        <Navbar/>
        <div className="container custom-livis-container">
            <div className="row">
                <div className="col-md-8 capture-img-wrap" >
                    {/* <p>Capture Image</p> */}
                    <img width="100%" height="100%" src="http://164.52.194.78:8000/livis/v1/toyoda/stream1/original_frame/" alt="N.A"/>
                    {/* <iframe width="100%" height="100%" src="http://164.52.194.78:8000/livis/v1/toyoda/stream1/original_frame/"></iframe> */}
                </div>

                <div className="col-md-3">
                <select id="inputState" class="form-control" value={this.state.part_number}  onChange={this.onChangePartNumber}>
                    <option>Select Part Number...</option>
                        {
                                this.state.parts.map(function(part) {
                                    return <option
                                    key={part['_id']}
                                    data-key = {part['_id']}
                                    value={part['part_number']} >{part['part_number']}
                                    </option>;
                                })
                                }
                </select>
                </div>
                <div className="col-md-1">
                    <button onClick={() => this.captureImage()} className="btn btn-info">Capture</button>
                </div>
            </div>

         </div>   
         

       
        </>

        
      
        )
    }
}