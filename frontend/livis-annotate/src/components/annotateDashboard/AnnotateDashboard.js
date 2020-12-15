import React from 'react'
import ReactImageAnnotate from "react-image-annotate"
import axios from 'axios'
import Navbar from '../navbar/Navbar'
import { ToastContainer, toast } from 'react-toastify';

export default class AnnotateDashboard extends React.Component{
  constructor(props){
    super(props)

    this.state = {
      image_info: null,
      part_id:null,
      img_id:null,
      inputValue:"",
      part_images:null,
    }

  }

  componentDidMount() {
    let search = window.location.search;
    let params = new URLSearchParams(search);
    let part_id = params.get('id');
    // let img_id = params.get('img_id');
    this.setState({part_id:part_id})
    // this.getImage(part_id,img_id);
    this.getPartImages(part_id,1,20);
  }

  getPartImages = async (part_id,current_page,limit) => {
    // await axios.get(window.$livis_config.API_URL+`fetch_data/?part_id=${part_id}&current=${current_page}&limit=${limit}`)
    await axios.get(window.$livis_config.API_URL+`fetch_data/?part_id=${part_id}`)
    .then(response => {
      console.log(typeof response.data.data);
      var part_image_list = response.data.data;
      var img_data = [];
      for (var key in part_image_list) {
        // console.log(part_image_list[key]);
        var temp_data = {}
        temp_data['id'] = part_image_list[key]._id;
        temp_data['src'] = part_image_list[key].file_url;
        temp_data['part_id'] = part_id;
        temp_data['regions'] = part_image_list[key].regions;

        img_data.push(temp_data);
        // if (p.hasOwnProperty(key)) {
        //     console.log(key + " -> " + p[key]);
        // }
      }
      // console.log(img_data);
    
      this.setState({part_images:img_data})
       // alert("ds");
    //    console.log(typeof response);
      // if (response != false) {
      //      this.setState({part_images:response.data})
      //      console.log(this.state.part_images);
      // }
    })
    .catch((error) => {
      console.log(error);
    })
  };

  // shouldComponentUpdate(nextProps, nextState) {
  //   console.log(nextProps, nextState);
  //   console.log(this.props, this.state);

  //   return true;  
  // }

  // componentDidUpdate()
  // {
  //   console.log("component did update");
  // }


  getImage = async (part_id,img_id) => {
    await axios.get(window.$livis_config.API_URL+`get_img/?part_id=${part_id}&file_id=${img_id}`)
    .then(response => {
      if (response != false) {
           this.setState({image_info:response.data.data,inputValue:response.data.data.classifier_label})
           
          //  console.log(response.data.);
      }
    })
    .catch((error) => {
      console.log(error);
    })
  };

  saveImage = (img_data)=>
  {
    // console.log(this.state.inputValue);

    // console.log(JSON.stringify(img_data));
    var post_data = img_data.images[img_data['selectedImage']];
    // console.log(typeof post_data);
    var tempProps = JSON.parse(JSON.stringify(post_data));
    tempProps.classifier_label = this.state.inputValue;
    Object.preventExtensions(tempProps);
    // if(this.state.inputValue != false){
      axios.post(window.$livis_config.API_URL+"submit_annotations/",tempProps
      ).then(res => { 
        // console.log(res);
       toast.success("Saved Successfully");
      }).catch((error) => {
        toast.error("Unknown Error");
      })
      // console.log(img_data.images[0]);
    // }else{
    //   toast.error("Please Add Label");
    // }
  }

  showNextPrevImage = async (output)=>
  {
    console.log(output);
    // var url = window.$livis_config.API_URL+`next_img/?part_id=${part_id}&file_id=${img_id}&type=${type}`;
    // if(type == "prev")
    // {
    //   url = window.$livis_config.API_URL+`prev_img/?part_id=${part_id}&file_id=${img_id}&type=${type}`;
    // }
    // await axios.get(url)
    // .then(response => {
    //   if (response != false) {
    //         // var 
    //        this.setState({image_info:response.data.data,inputValue:response.data.data.classifier_label})
    //       //  this.forceUpdate();
    //       //  this.shouldComponentUpdate;
    //       //  this.forceUpdate();

    //       //  console.log("dd",response.data.data);
    //   }
    // })
    // .catch((error) => {
    //   console.log(error);
    // }) 
  }


  updateInputValue = (evt)=> {
    this.setState({
      inputValue: evt.target.value
    });
  }

render(){
  
  const annotateimg = this.state.part_images?<ReactImageAnnotate
  cache={false}
  selectedImage={this.state.part_images[0].src}
  taskDescription=""
  images={this.state.part_images}
  regionClsList={["Classification", "Hole"]}
  regionTagList= {["tag1", "tag2"]}
  onExit={output => {
          this.saveImage((output));
        }}
  // onNextImage={output => {
  //   // console.log(output);
  //   // return true;
  // }}        
  // onNextImage={output1 => {
  //  (this.showNextPrevImage(this.state.part_id,this.state.image_info._id,'next'));
  // }}  
  // onPrevImage={output1 => {
  //     (this.showNextPrevImage(this.state.part_id,this.state.image_info._id,'prev'));
  // }}     
    
    
/>:""
// console.log(this.state.image_info);
const annotateForm = this.state.part_images?
<div className="row m-2">
 
  <div className="col-md-3 custom-label-position">
    <input type="text" value={this.state.inputValue} onChange={this.updateInputValue} className="form-control" placeholder="Add Label"/>

  </div>
  <div className="col-md-5">

  </div>
  <div className="col-md-3 text-right">
    <select className="form-control">
        <option>XML</option>
        <option>CSV</option>

    </select>
   
  </div>
  <div className="col-md-1 text-right">
 
    <button className="btn btn-info">Export</button>
  </div>
</div>:""
return(
 
<>

<ToastContainer />
<Navbar/>
<div className="custom-livis-container">
{annotateForm}
{annotateimg}
</div>
  </>
)







}
}


