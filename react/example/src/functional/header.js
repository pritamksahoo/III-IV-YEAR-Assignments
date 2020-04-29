import React, { Component } from 'react';
import { Link } from 'react-router-dom';

const compObj = [
    {
        id: 1,
    },
    {
        id: 2,
    },
    {
        id: 3,
    }
]

class Header extends Component {
    render() {
        return (
            <div>
                <Link to="/">Home </Link>
                {compObj.map((item) => {
                    return (
                        <Link key={item.id} to={{pathname: '/component/' + item.id}}> | Component{item.id} </Link>
                    )
                })}
                <br></br>
                <hr></hr>
            </div>
        )
    }
}

export default Header;