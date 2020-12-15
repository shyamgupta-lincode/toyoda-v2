import React from 'react'
import axios from 'axios'
import { Link, NavLink, Redirect } from 'react-router-dom'
//import './user/signin.css'

const Dropdown =(props)=>(
  <div>

  <ul  className="navbar navbar-nav float-right">
              <li className="nav-item dropdown">
                <a className="nav-link dropdown-toggle" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                  {localStorage.getItem('username')}
        </a>
                <div className="dropdown-menu" aria-labelledby="navbarDropdownMenuLink">
                  <a className="dropdown-item" href="#">Profile</a>
                  <a className="dropdown-item"><Link to="/logout">LogOut</Link></a>

                </div>
              </li>

            </ul>

  </div>

)

export default class Navbar extends React.Component {
          constructor(props){
            super(props)


            const token = localStorage.getItem('token');
            let isVisible="d-none"

            if(token!=null){
              isVisible="d-print-block"
            }
            this.state={
              isVisible
            }

          }





         showUser(){
          return <Dropdown />
         }

  render() {
    //console.log(this.state.isVisible)
    return (

      <div className="custom-livis-header">
        <nav className="navbar1" >

        <div class="header-container">
          <div class="livis-logo-container">
          <a href="http://localhost:4200/livis/apps" class="logo no-padding">
            <img src="/logo.png" class="livis-logo no-padding"/> | Livis Annotate
          </a>
          </div>

        </div>
          {/* <a className="navbar-brand" >Livis Image Annotate</a>
          <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarText" aria-controls="navbarText" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>

            <div className={this.state.isVisible}   > */}
            {/* {this.showUser()} */}
            {/* </div> */}


        </nav>
      </div>
    )
  }
}