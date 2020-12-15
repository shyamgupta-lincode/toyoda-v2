import React from 'react'
import {Helmet} from 'react-helmet';
import axios from 'axios'
import ImageGallery from 'react-image-gallery';
import './userDashboard.css'
import Navbar from '../navbar/Navbar'



export default class UserDashboard extends React.Component{
constructor(props){
    super(props)

    this.onChangePartNumber = this.onChangePartNumber.bind(this);
    this.onChangeFile = this.onChangeFile.bind(this);
    this.onHandleSubmit = this.onHandleSubmit.bind(this);

    this.state = {
    _id:'',
    numberOfImages:0,
    file:'Choose File',
    selectedFile:null,
    part_number:'',
    part_description:'',
    parts:[{
"_id": "5f2d3b2be0314f1560a2338b",
"short_number": "IG98",
"model_number": "579W",
"planned_production": null,
"part_number": "622120K180B0",
"part_description": "FR PILLAR LH WITH SRS\n",
"edit_part_data": "",
"isdeleted": false,
"kanban": null
},
{
"_id": "5f2d3b2be0314f1560a2338b",
"short_number": "IG98",
"model_number": "579W",
"planned_production": null,
"part_number": "622120K180A0",
"part_description": "FR PILLAR LH WITH SRA\n",
"edit_part_data": "",
"isdeleted": false,
"kanban": null
},

{
"_id": "5f2d3b2be0314f1560a2338b",
"short_number": "IG98",
"model_number": "579W",
"planned_production": null,
"part_number": "622120K180C0",
"part_description": "FR PILLAR LH WITH SRB\n",
"edit_part_data": "",
"isdeleted": false,
"kanban": null
}


],

images : []
  }
  }

  onChangePartNumber(e) {
  let part_desc=''
  let id=''
  this.state.parts.map(function(part) {
        if(part['part_number']===e.target.value){
            part_desc= part['part_description']
            id=part['_id']

        }
    })
    this.setState({
      part_number: e.target.value,
      part_description:part_desc,
      _id:id


    });


  }

  onChangeFile(e){
    //value={this.state.file} onChange={this.onChangeFile}
    this.setState({
    file:e.target.files[0].name,
    selectedFile:e.target.files[0],
    loaded: 0
    })

  console.log(e.target.files)
  }


  onHandleSubmit = () => {
   const data = new FormData()
   data.append('myfile', this.state.selectedFile)
   data.append('part_id',this.state._id)
//   const sendInfo={
//    data,
//    "_id":this.state._id
//   }
   //console.log(sendInfo)
   if(this.state.part_number!=='' && this.state.selectedFile!==null){
   axios.post("http://127.0.0.1:8000/livis/v1/Livis_annotate/upload_annotations/",data
      // receive two    parameter endpoint url ,form data

  )
  .then(res => { // then print response status
    console.log(res.data.image_urls)
    this.setState({
        images:res.data.image_urls
    })
 })
 }else{
    alert("Please fill all the details")
 }
}



  render(){
  return(
  <div>
  <Navbar/>
  <div className="container">
  <Helmet>
                {/*<style>{'body { background-color: red; }'}</style>*/}
   </Helmet>

<div className="card"  id="top_card">
  <div className="card-body">

  <div class="form-row">
    <div class="form-group col-md-4">
      <label for="inputState">Part ID</label>
      <select id="inputState" class="form-control" value={this.state.part_number}  onChange={this.onChangePartNumber}>
      <option>Choose Part Number...</option>
        {
                  this.state.parts.map(function(part) {
                    return <option
                      key={part['part_number']}
                      value={part['part_number']} >{part['part_number']}
                      </option>;
                  })
                }
      </select>
    </div>
    <div class="form-group col-md-4">
      <label for="inputPartName">Part Description</label>
      <input type="text" class="form-control" value={this.state.part_description} id="inputPartDescription"/>
    </div>
  </div>

  <div class="form-row">
    <div class="form-group col-md-4">
      <label for="inputCity">Upload Zip file</label>
      <div class="custom-file">
    <input type="file" class="custom-file-input" accept=".zip" id="inputGroupFile02"  onChange={this.onChangeFile} />
    <label class="custom-file-label" for="inputGroupFile02"  aria-describedby="inputGroupFileAddon02">{this.state.file}</label>
  </div>
    </div>

  </div>

  <button type="button" class="btn btn-primary" onClick={this.onHandleSubmit}>Submit</button>



  </div>

  </div>

{/*===========Render Images===========*/}
<div id="imageThumbnail">
<div className="row">
{
this.state.images.map(function(image) {

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




  {/*===========Render Images ENd===========*/}

  </div>



  </div>

  )
  }

  }