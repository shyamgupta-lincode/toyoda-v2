import React from 'react'
import ReactPaginate from 'react-paginate';

import PartNumber from './partNumber/PartNumber';
import axios from 'axios';


export default class PartNumberDashboard extends React.Component {
    constructor(props){
        super(props);

        this.handlePageClick = this
            .handlePageClick
            .bind(this);
        let partNumberList=[]

        for(let i=0;i<50;i++){

        partNumberList.push(i)
        }

        this.state={
        offset: 0,
      data: [],
      perPage: 5,
      currentPage: 0,
            partNumberList
        };

    }


    receivedData() {
        axios.get("https://jsonplaceholder.typicode.com/photos")
            .then(res => {

                const data = res.data;
                const slice = data.slice(this.state.offset, this.state.offset + this.state.perPage)
                const postData = slice.map(pd => <React.Fragment>
                    <p>{pd.title}</p>
                    <img src={pd.thumbnailUrl} alt=""/>
                </React.Fragment>)

                this.setState({
                    pageCount: Math.ceil(data.length / this.state.perPage),

                    postData
                })
            });
    }

    handlePageClick = (e) => {
        const selectedPage = e.selected;
        const offset = selectedPage * this.state.perPage;

        this.setState({
            currentPage: selectedPage,
            offset: offset
        }, () => {
            this.receivedData()
        });

    };

    componentDidMount(){
this.receivedData()

    }



    render(){
        return(
            <>


{this.state.postData}
            <ReactPaginate
                    previousLabel={"prev"}
                    nextLabel={"next"}
                    breakLabel={"..."}
                    breakClassName={"break-me"}
                    pageCount={this.state.pageCount}
                    marginPagesDisplayed={2}
                    pageRangeDisplayed={5}
                    onPageChange={this.handlePageClick}
                    containerClassName={"pagination"}
                    subContainerClassName={"pages pagination"}
                    activeClassName={"active"}/>


            </>
            
        )
    }
}