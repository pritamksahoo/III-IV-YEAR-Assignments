import React, {Component} from 'react';
import './keypad.css';

class Keypad extends Component {

    render = () => {
        return (
            <div id={this.props.id} key={this.props.id} className={this.props.class} onClick={this.props.onclick}>
                {this.props.icon}
            </div>
        )
    }
}

export {Keypad};