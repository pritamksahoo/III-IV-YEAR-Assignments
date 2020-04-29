import React, { Component } from 'react';

const Component1 = (props) => {
    console.log("Component1 => ", props)
    return (
        <div>Component{props.match.params.id}</div>
    )
}

export default Component1;