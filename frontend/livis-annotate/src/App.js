import React from 'react';
import {BrowserRouter as Router, Route, Link, Redirect} from 'react-router-dom';

import PartNumberDashboard from './components/partNumber/PartNumber'
import AnnotateDashboard from './components/annotateDashboard/AnnotateDashboard'
import ImageDashboard from './components/imagesDashboard/ImagesDashboard'
import Navbar from './components/navbar/Navbar'
import UserDashboard from './components/user/UserDashboard'
import Capture from './components/capture/Capture'

import Home from './components/home/Home'


function App() {
  return (
    <Router>
     
      <Route path="/" exact component={Home} />
      {/* <Route path="/home" exact component={Home} /> */}

      <Route path="/annotate"  component={AnnotateDashboard} />
      <Route path="/image_dashboard"  component={ImageDashboard} />
      <Route path="/capture"  component={Capture} />


      
      
    </Router>
  );
}

export default App;
