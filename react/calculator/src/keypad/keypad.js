import React, {Component} from 'react';
import {digit} from './digit';
import './keypad.css';

class Keypad extends Component {

    digitDiv = digit.map((item) => {
        return (
            <div id={item.id} key={item.id} className={item.class}>
                {item.icon}
            </div>
        )
    })

    render = () => {
        return (
            <div className="Keypad">
                {this.digitDiv}
            </div>
        )
    }
}

export {Keypad};