import React from 'react'
// import { BrowserRouter as Router, Route, Link, Switch, useParams } from "react-router-dom"
import Navbar from '../navbar/Navbar'
import axios from 'axios'
import {
  
    Modal,
 
    } from "reactstrap";
import Pagination from "react-js-pagination";
import { ToastContainer, toast } from 'react-toastify';
export default class Home extends React.Component{
    

    constructor(props){
        super(props)
       
        // console.log("query",query_data);
        this.state = {
            showUploadModal:false,
            file:'Choose File',
            selectedFile:null,
            part_id:null,
            part_images:null,
            activePage:1,
            per_page:20,
            upload_button_text:'Upload',
            

            // loaded
       }
    }


 componentDidMount() {
    let search = window.location.search;
    let params = new URLSearchParams(search);
    let part_id = params.get('part_id');
    // alert(part_id);
    if(part_id == null)
    {
      // alert("dd")
      window.location.href = window.$livis_config.TRAINING_WEB_URL;
    }
    // const query_data = useParams()
    // console.log("query",search);
   
    // 5f42b5a90b72e674c03691d5
    this.setState({part_id:part_id})
    this.getPartImages(part_id,this.state.activePage,this.state.per_page);

 }


 getPartImages = async (part_id,current_page,limit) => {
    await axios.get(window.$livis_config.API_URL+`fetch_data/?part_id=${part_id}&current=${current_page}&limit=${limit}`)
    .then(response => {
       // alert("ds");
    //    console.log(typeof response);
      if (response != false) {
           this.setState({part_images:response.data})
           console.log(this.state.part_images);
      }
    })
    .catch((error) => {
      console.log(error);
    })
  };


    

    uploadFileModel = (status)=>{
        this.setState({showUploadModal:status})
    }

    onChangeFile = (e)=>{
        console.log(e);
        //value={this.state.file} onChange={this.onChangeFile}
        this.setState({
        file:e.target.files[0].name,
        selectedFile:e.target.files[0],
        // loaded: 0
        })
      console.log(e.target.files)
    }

    onHandleSubmit = (event) => {
        // event.preventDefault();
        const data = new FormData()
        data.append('myfile', this.state.selectedFile)
        data.append('part_id',this.state.part_id)
        if(this.state.part_number!=='' && this.state.selectedFile!==null){
          this.setState({upload_button_text:"Uploading..."})
        axios.post(window.$livis_config.API_URL+"create_dataset/",data
           // receive two    parameter endpoint url ,form data
          
       )
       .then(res => { // then print response status
        // this.setState({
        //      images:res.data.image_urls
        //  })
        this.setState({upload_button_text:"Upload"})
        this.uploadFileModel(false);
        this.getPartImages(this.state.part_id,1,20);
        toast.success("Uploaded Successfully");

        //  console.log(res.data.image_urls)
       
      })
      }else{
        toast.error("Please Upload The Files");
        //  alert("Please fill all the details")
      }
    }

    handlePageChange(pageNumber) {
        console.log(`active page is ${pageNumber}`);
        this.setState({activePage: pageNumber});
        this.getPartImages(this.state.part_id,pageNumber,this.state.per_page);
    }
    

    render(){
        // console.log(this.state);
        var custom_part_id = this.state.part_id;
        const imageList = this.state.part_images?this.state.part_images.data.map(function(current_value,index) {
            // console.log(value)

            return  <div key={index} className="col-md-3">
            <div className="card part-img-card">
            <div className="card-body">
        {/* <div className ="thumbnail"> */}
            <a href={"/annotate?id="+custom_part_id} >
            <img className="img-thumbnail" src={current_value.file_url} alt="part image" />
            </a>
        {/* </div> */}
        </div>
    </div>
    </div>
     }):"Not Found";

     const paging_info = this.state.part_images && this.state.part_images.total > 20 ?<Pagination
     itemClass="page-item"
     linkClass="page-link"
     activePage={this.state.activePage}
     itemsCountPerPage={this.state.per_page}
     totalItemsCount={this.state.part_images.total}
     pageRangeDisplayed={5}
     onChange={this.handlePageChange.bind(this)}
     />:"";
        return(
        <>
         <ToastContainer />
        <Navbar/>
        <div className="container custom-livis-container">
            <div className="row upload-button-wrap">
                <button onClick={() => this.uploadFileModel(true)} className="btn btn-info">Upload</button>
            </div>

            <div className="row">
            {imageList}
            </div>

            <div className="row pagination-wrap">
              {paging_info}
            </div> 
         </div>   
         

         <Modal
          className="modal-dialog-centered"
          isOpen={this.state.showUploadModal}
        //   size="lg"
          aria-labelledby="example-modal-sizes-title-lg"
        //   centered
        >
          <div className="modal-header"  id="modal-title-notification">
            <h4 className="modal-title text-center">
              Upload Image
            </h4>
            <button
              aria-label="Close"
              className="close"
              data-dismiss="modal"
              type="button"
              onClick={() => this.uploadFileModel(false)}
            >
              <span aria-hidden={true} id="modal-cross">×</span>
            </button>
          </div>
        <form>
            <div className="modal-body">
                <div class="form-group">
                    <label for="inputCity">Upload Zip file</label>
                    <div class="custom-file">
                    <input type="file" className="custom-file-input" accept=".zip" id="inputGroupFile02"  onChange={this.onChangeFile} />
                    <label className="custom-file-label" for="inputGroupFile02"  aria-describedby="inputGroupFileAddon02">{this.state.file}</label>
                    </div>
                </div>
            </div>
            <div className="modal-footer">
            <button
                type="button"
                className = "btn btn-warning"
                onClick={() => this.uploadFileModel(false)}
                >
                Close
            </button>   

            <button type="button" onClick={() => this.onHandleSubmit()} className="btn btn-info ml-auto" color="info" > {this.state.upload_button_text}</button>
            
            </div>
        </form>

        
        </Modal>
        </>

        
      
        )
    }
}